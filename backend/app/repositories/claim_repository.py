from uuid import UUID

from sqlalchemy import select

from app.models.claim import ClaimModel
from app.repositories.base_repository import BaseRepository


class ClaimRepository(BaseRepository):

    async def create(self, claim: ClaimModel):

        self.db.add(claim)

        await self.db.commit()

        await self.db.refresh(claim)

        return claim

    async def get_by_id(self, claim_id: UUID):

        query = select(ClaimModel).where(
            ClaimModel.id == claim_id
        )

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def update_status(
        self,
        claim_id: UUID,
        status: str
    ):

        claim = await self.get_by_id(claim_id)

        if not claim:
            return None

        claim.status = status

        await self.db.commit()

        await self.db.refresh(claim)

        return claim