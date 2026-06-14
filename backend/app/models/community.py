"""
社區功能模型
支持策略分享、討論、用戶互動
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
from uuid import uuid4


class ContentType(str, Enum):
    STRATEGY = "strategy"
    DISCUSSION = "discussion"
    ANALYSIS = "analysis"
    NEWS = "news"


class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    DELETED = "deleted"


class ReportReason(str, Enum):
    SPAM = "spam"
    HARASSMENT = "harassment"
    MISLEADING = "misleading"
    INAPPROPRIATE = "inappropriate"
    OTHER = "other"


class User(BaseModel):
    """用戶"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    username: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: str = ""
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    reputation: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    is_verified: bool = False


class Post(BaseModel):
    """貼文"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    author_id: str
    content_type: ContentType
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)
    
    # 互動數據
    likes_count: int = 0
    comments_count: int = 0
    views_count: int = 0
    shares_count: int = 0
    
    # 狀態
    status: PostStatus = PostStatus.PUBLISHED
    is_pinned: bool = False
    is_featured: bool = False
    
    # 元數據
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # 附加數據（策略專用）
    extra_data: Dict[str, Any] = Field(default_factory=dict)


class Comment(BaseModel):
    """評論"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    post_id: str
    author_id: str
    parent_id: Optional[str] = None  # 回覆評論
    content: str
    likes_count: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    is_hidden: bool = False


class Like(BaseModel):
    """點讚"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    target_id: str  # post_id 或 comment_id
    target_type: str  # "post" 或 "comment"
    created_at: datetime = Field(default_factory=datetime.now)


class Follow(BaseModel):
    """關注"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    follower_id: str
    following_id: str
    created_at: datetime = Field(default_factory=datetime.now)


class Report(BaseModel):
    """舉報"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    reporter_id: str
    target_id: str
    target_type: str  # "post" 或 "comment" 或 "user"
    reason: ReportReason
    description: str = ""
    status: str = "pending"  # pending, reviewed, resolved, dismissed
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)


class StrategyShare(Post):
    """策略分享"""
    content_type: ContentType = ContentType.STRATEGY
    
    # 策略數據
    entry_rules: str = ""
    exit_rules: str = ""
    risk_management: str = ""
    backtest_results: Optional[Dict[str, Any]] = None
    performance_metrics: Dict[str, float] = Field(default_factory=dict)
