from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, status, Query, Security

from app.schemas.message import (
    MessageCreate,
    MessageResponse,
    EncryptedMessageResponse,
    DecryptAttemptResponse,
    MessageListResponse,
)
from app.domain.entities.user import User
from app.domain.errors import NotFoundError
from app.api.dependencies import get_current_active_user, get_message_repository
from app.infrastructure.repositories.message_repository import MessageRepository
from app.application.usecases.message_usecases import (
    CreateMessageUseCase,
    GetAllyMessagesUseCase,
    InterceptEnemyMessageUseCase,
    DecryptMessageUseCase,
)


router = APIRouter(prefix="/messages", tags=["Messages (Spy Mini-Game)"])


def message_to_response(message) -> MessageResponse:
    """Convert EncryptedMessage entity to MessageResponse schema."""
    return MessageResponse(
        id=message.id,
        author_id=message.author_id,
        text=message.original_text,
        alignment=message.alignment,
        created_at=message.created_at,
    )


@router.post(
    "/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create encrypted message",
    description="Create a new message that will be visible to your allies and encrypted for enemies to intercept.",
)
async def create_message(
    message_data: MessageCreate,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:read"])],
    message_repository: Annotated[MessageRepository, Depends(get_message_repository)],
):
    """Create a new encrypted message for the spy game."""
    if current_user.alignment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have an alignment (light/dark) to send messages",
        )

    use_case = CreateMessageUseCase(repository=message_repository)
    message = await use_case.execute(
        author_id=current_user.id,
        text=message_data.text,
        alignment=current_user.alignment,
    )
    return message_to_response(message)


@router.get(
    "/",
    response_model=MessageListResponse,
    summary="Get ally messages",
    description="Retrieve messages from your side of the Force. Only shows messages from your alignment.",
)
async def get_ally_messages(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:read"])],
    message_repository: Annotated[MessageRepository, Depends(get_message_repository)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    sort_by: Literal["created_at"] = Query("created_at", description="Field to sort by"),
    sort_order: Literal["asc", "desc"] = Query("desc", description="Sort order: 'asc' or 'desc'"),
):
    """Get messages from your side."""
    if current_user.alignment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have an alignment (light/dark) to view messages",
        )

    use_case = GetAllyMessagesUseCase(repository=message_repository)
    messages, count = await use_case.execute(
        alignment=current_user.alignment,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    
    return MessageListResponse(
        count=count,
        results=[message_to_response(m) for m in messages],
    )


@router.post(
    "/intercept",
    response_model=EncryptedMessageResponse,
    summary="Intercept enemy message",
    description="Intercept a random encrypted message from the enemy side. Returns an encrypted message that you can try to decrypt.",
)
async def intercept_enemy_message(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:read"])],
    message_repository: Annotated[MessageRepository, Depends(get_message_repository)],
):
    """Intercept a random enemy message."""
    if current_user.alignment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have an alignment (light/dark) to intercept messages",
        )

    use_case = InterceptEnemyMessageUseCase(repository=message_repository)
    message = await use_case.execute(user_alignment=current_user.alignment)
    
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No enemy messages available to intercept",
        )
    
    return EncryptedMessageResponse(
        id=message.id,
        encrypted_text=message.encrypted_text,
        alignment=message.alignment,
        created_at=message.created_at,
    )


@router.post(
    "/{message_id}/decrypt",
    response_model=DecryptAttemptResponse,
    summary="Attempt to decrypt message",
    description="Try to decrypt an intercepted message. Returns partially revealed text (1/6 to 4/6 of letters) in format '_a_b_c'.",
)
async def decrypt_message(
    message_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["users:read"])],
    message_repository: Annotated[MessageRepository, Depends(get_message_repository)],
):
    """Attempt to decrypt an intercepted message."""
    if current_user.alignment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User must have an alignment (light/dark) to decrypt messages",
        )

    use_case = DecryptMessageUseCase(repository=message_repository)
    
    try:
        partial_text, is_complete = await use_case.execute(
            message_id=message_id,
            user_alignment=current_user.alignment,
        )
        return DecryptAttemptResponse(
            partial_text=partial_text,
            is_complete=is_complete,
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or you cannot decrypt your own side's messages",
        )
