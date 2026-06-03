from sqlalchemy import select

from app.models.trace import TraceEventModel

from app.repositories.base_repository import BaseRepository


class TraceRepository(BaseRepository):

    async def create(
        self,
        trace: TraceEventModel
    ):

        self.db.add(trace)

        await self.db.commit()

        await self.db.refresh(trace)

        return trace

    async def get_claim_trace(
        self,
        claim_id
    ):

        query = select(
            TraceEventModel
        ).where(
            TraceEventModel.claim_id == claim_id
        )

        result = await self.db.execute(query)

        return result.scalars().all()