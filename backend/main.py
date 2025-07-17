from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import IntegrityError
from models import Feature, Vote, FeatureCreate, FeatureResponse, VoteCreate, VoteResponse, ErrorResponse
from typing import List
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Feature Voting API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql://appuser:apppassword@localhost:3306/feature_voting")


@app.post("/features", response_model=FeatureResponse, status_code=status.HTTP_201_CREATED)
async def create_feature(feature_data: FeatureCreate):
    """Create a new feature"""
    try:
        # Validate input data
        if not feature_data.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty"
            )

        if not feature_data.description.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description cannot be empty"
            )

        # Create feature
        feature = await Feature.create(
            title=feature_data.title.strip(),
            description=feature_data.description.strip(),
            created_by=feature_data.created_by.strip()
        )

        logger.info(f"Created feature with ID: {feature.id}")

        return FeatureResponse(
            id=feature.id,
            title=feature.title,
            description=feature.description,
            created_by=feature.created_by,
            created_at=feature.created_at,
            vote_count=feature.vote_count
        )

    except Exception as e:
        logger.error(f"Error creating feature: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.post("/votes", response_model=VoteResponse, status_code=status.HTTP_201_CREATED)
async def vote_feature(vote_data: VoteCreate):
    """Vote for a feature"""
    try:
        # Check if feature exists
        feature = await Feature.get_or_none(id=vote_data.feature_id)
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feature not found"
            )

        # Validate voter_id
        if not vote_data.voter_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Voter ID cannot be empty"
            )

        # Create vote (will fail if user already voted due to unique constraint)
        vote = await Vote.create(
            feature_id=vote_data.feature_id,
            voter_id=vote_data.voter_id.strip()
        )

        # Update vote count
        feature.vote_count += 1
        await feature.save()

        logger.info(f"Vote created with ID: {vote.id} for feature: {vote_data.feature_id}")

        return VoteResponse(
            id=vote.id,
            feature_id=vote.feature_id,
            voter_id=vote.voter_id,
            created_at=vote.created_at
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User has already voted for this feature"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating vote: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/features", response_model=List[FeatureResponse])
async def get_features():
    """Get all features"""
    try:
        features = await Feature.all().order_by('-created_at')

        return [
            FeatureResponse(
                id=feature.id,
                title=feature.title,
                description=feature.description,
                created_by=feature.created_by,
                created_at=feature.created_at,
                vote_count=feature.vote_count
            )
            for feature in features
        ]

    except Exception as e:
        logger.error(f"Error fetching features: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/features/{feature_id}", response_model=FeatureResponse)
async def get_feature(feature_id: int):
    """Get a specific feature"""
    try:
        feature = await Feature.get_or_none(id=feature_id)
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feature not found"
            )

        return FeatureResponse(
            id=feature.id,
            title=feature.title,
            description=feature.description,
            created_by=feature.created_by,
            created_at=feature.created_at,
            vote_count=feature.vote_count
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching feature: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Register Tortoise ORM
register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)