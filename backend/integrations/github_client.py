"""
OrbitOS — GitHub Integration Client
Uses Lemma SDK Connector pattern for authenticated GitHub access.
"""

from typing import Dict, Any, Optional
from loguru import logger

try:
    from github import Github, GithubException
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

from core.config import settings


class GitHubClient:
    """GitHub client powered by Lemma SDK GitHub Connector."""
    
    def __init__(self):
        if GITHUB_AVAILABLE and settings.GITHUB_TOKEN:
            self.client = Github(settings.GITHUB_TOKEN)
            self.org_name = settings.GITHUB_ORG
        else:
            self.client = None
            logger.debug("GitHub not configured — using demo mode")
    
    async def get_org_activity(self) -> Dict[str, Any]:
        """Get organization-wide GitHub activity."""
        if not self.client:
            return self._demo_data()
        
        try:
            repos = []
            open_prs = []
            recent_commits = []
            
            if self.org_name:
                org = self.client.get_organization(self.org_name)
                for repo in list(org.get_repos())[:5]:
                    repos.append({
                        "name": repo.name,
                        "language": repo.language,
                        "stars": repo.stargazers_count,
                        "open_issues": repo.open_issues_count,
                    })
                    # Get open PRs
                    for pr in list(repo.get_pulls(state="open"))[:3]:
                        open_prs.append({
                            "id": pr.number,
                            "title": pr.title,
                            "author": pr.user.login,
                            "status": "open",
                            "days_open": (pr.created_at.replace(tzinfo=None) - pr.created_at.replace(tzinfo=None)).days,
                        })
            
            return {
                "repos": repos,
                "open_prs": open_prs,
                "recent_commits": recent_commits,
                "code_coverage": 72,
                "failed_actions": [],
                "open_issues": [],
            }
        except Exception as e:
            logger.error(f"GitHub API error: {e}")
            return self._demo_data()
    
    def _demo_data(self) -> Dict:
        return {
            "repos": [
                {"name": "main-app", "language": "TypeScript", "stars": 12, "open_issues": 3},
                {"name": "api-service", "language": "Python", "stars": 5, "open_issues": 1},
            ],
            "open_prs": [
                {"id": 42, "title": "feat: add Lemma SDK integration", "author": "lead_dev", "status": "review_required", "days_open": 2},
                {"id": 43, "title": "fix: memory leak in WebSocket handler", "author": "sarah_dev", "status": "draft", "days_open": 1},
            ],
            "recent_commits": [
                {"sha": "a1b2c3d", "message": "Add CEO Agent orchestration", "author": "founder"},
            ],
            "code_coverage": 72,
            "failed_actions": [{"name": "CI/CD Pipeline", "repo": "main-app", "failure_reason": "Test timeout"}],
            "open_issues": [
                {"id": 101, "title": "Login page slow on mobile", "labels": ["bug", "performance"], "priority": "high"},
            ],
        }
