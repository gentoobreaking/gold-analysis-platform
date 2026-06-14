"""
社區服務
提供貼文、評論、點讚、關注功能
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
import json
from pathlib import Path

from ..models.community import (
    Post, Comment, Like, Follow, Report, User,
    ContentType, PostStatus, ReportReason
)


class CommunityService:
    """社區服務"""
    
    def __init__(self, data_dir: str = "./data/community"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self._posts: Dict[str, Post] = {}
        self._comments: Dict[str, Comment] = {}
        self._users: Dict[str, User] = {}
        
        self._load_all()
    
    def _load_all(self) -> None:
        for file in self.data_dir.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("type") == "post":
                    self._posts[data["id"]] = Post(**data)
                elif data.get("type") == "user":
                    self._users[data["id"]] = User(**data)
    
    def _save(self, obj: Any, obj_type: str) -> None:
        path = self.data_dir / f"{obj.id}.json"
        data = obj.model_dump(mode="json")
        data["type"] = obj_type
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    # === 用戶 ===
    
    def create_user(self, username: str, display_name: Optional[str] = None) -> User:
        user = User(username=username, display_name=display_name or username)
        self._users[user.id] = user
        self._save(user, "user")
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    # === 貼文 ===
    
    def create_post(
        self,
        author_id: str,
        title: str,
        content: str,
        content_type: ContentType = ContentType.DISCUSSION,
        tags: List[str] = None
    ) -> Post:
        post = Post(
            author_id=author_id,
            title=title,
            content=content,
            content_type=content_type,
            tags=tags or []
        )
        self._posts[post.id] = post
        self._save(post, "post")
        return post
    
    def get_post(self, post_id: str) -> Optional[Post]:
        return self._posts.get(post_id)
    
    def list_posts(
        self,
        content_type: ContentType = None,
        author_id: str = None,
        limit: int = 20
    ) -> List[Post]:
        posts = list(self._posts.values())
        
        if content_type:
            posts = [p for p in posts if p.content_type == content_type]
        if author_id:
            posts = [p for p in posts if p.author_id == author_id]
        
        posts = [p for p in posts if p.status == PostStatus.PUBLISHED]
        return sorted(posts, key=lambda x: x.created_at, reverse=True)[:limit]
    
    def like_post(self, post_id: str, user_id: str) -> bool:
        post = self.get_post(post_id)
        if not post:
            return False
        post.likes_count += 1
        self._save(post, "post")
        return True
    
    # === 評論 ===
    
    def add_comment(
        self,
        post_id: str,
        author_id: str,
        content: str,
        parent_id: Optional[str] = None
    ) -> Comment:
        comment = Comment(
            post_id=post_id,
            author_id=author_id,
            parent_id=parent_id,
            content=content
        )
        self._comments[comment.id] = comment
        
        post = self.get_post(post_id)
        if post:
            post.comments_count += 1
            self._save(post, "post")
        
        return comment
    
    def get_comments(self, post_id: str) -> List[Comment]:
        return [c for c in self._comments.values() if c.post_id == post_id]
    
    # === 舉報 ===
    
    def report_content(
        self,
        reporter_id: str,
        target_id: str,
        target_type: str,
        reason: ReportReason,
        description: str = ""
    ) -> Report:
        report = Report(
            reporter_id=reporter_id,
            target_id=target_id,
            target_type=target_type,
            reason=reason,
            description=description
        )
        # TODO: 保存舉報記錄
        return report
