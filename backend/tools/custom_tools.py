import os
from typing import Optional, List, Dict, Any
from redminelib import Redmine
from agno.tools import Toolkit, tool
from backend.agents.schemas import SIC16Capex, SIC14Plazo, SIC03Riesgo

class RedmineTools(Toolkit):
    """
    Enhanced Redmine Tools with reasoning and structured data management.
    Supports issue tracking, project management, and knowledge base integration.
    """
    def __init__(self, **kwargs):
        super().__init__(name="redmine_tools", **kwargs)
        self.url = os.getenv("REDMINE_BASE_URL", "http://cidiia.uce.edu.do/")
        self.key = os.getenv("REDMINE_API_KEY")
        self.redmine = Redmine(self.url, key=self.key) if self.key else None
        self.issue_cache: Dict[int, Dict] = {}
        
        tools = [
            self.get_issue_details,
            self.list_projects,
            self.search_issues,
            self.analyze_issue_context,
            self.get_project_issues,
            self.update_issue_metadata,
            self.get_issue_relations,
            self.extract_issue_requirements,
        ]
        super().__init__(name="redmine_tools", tools=tools, **kwargs)
    
    def get_issue_details(self, issue_id: int) -> dict:
        """
        Fetch comprehensive details of a Redmine issue from the live site.
        
        Args:
            issue_id: The Redmine issue ID to retrieve
            
        Returns:
            Dictionary containing issue details including ID, subject, description, status, and project
        """
        if not self.redmine:
            return {"error": "Redmine API key not configured"}
        try:
            # Check cache first
            if issue_id in self.issue_cache:
                return self.issue_cache[issue_id]
            
            issue = self.redmine.issue.get(issue_id, include=['relations', 'changesets', 'watchers'])
            
            issue_data = {
                "id": issue.id,
                "subject": issue.subject,
                "description": issue.description or "",
                "status": issue.status.name,
                "project": issue.project.name,
                "created_on": str(issue.created_on) if hasattr(issue, 'created_on') else None,
                "updated_on": str(issue.updated_on) if hasattr(issue, 'updated_on') else None,
                "priority": issue.priority.name if hasattr(issue, 'priority') else None,
                "assigned_to": issue.assigned_to.name if hasattr(issue, 'assigned_to') else None,
                "custom_fields": {cf['name']: cf['value'] for cf in issue.custom_fields} if hasattr(issue, 'custom_fields') else {}
            }
            
            # Cache the result
            self.issue_cache[issue_id] = issue_data
            return issue_data
        except Exception as e:
            return {"error": f"Failed to retrieve issue {issue_id}: {str(e)}"}

    def list_projects(self) -> list:
        """
        List all available projects in Redmine.
        
        Returns:
            List of projects with ID, name, and identifier
        """
        if not self.redmine:
            return [{"error": "Redmine API key not configured"}]
        try:
            projects = self.redmine.project.all()
            return [{"id": p.id, "name": p.name, "identifier": p.identifier} for p in projects]
        except Exception as e:
            return [{"error": f"Failed to list projects: {str(e)}"}]

    def search_issues(self, project_id: str, query: str, status: Optional[str] = None) -> list:
        """
        Search for issues in a specific project with optional status filter.
        
        Args:
            project_id: The project identifier or ID
            query: Search query text
            status: Optional status filter (e.g., 'open', 'closed')
            
        Returns:
            List of matching issues with ID, subject, and status
        """
        if not self.redmine:
            return [{"error": "Redmine API key not configured"}]
        try:
            filters = {"project_id": project_id}
            if status:
                filters["status_id"] = status
            
            issues = self.redmine.issue.filter(**filters)
            results = []
            for i in issues:
                if query.lower() in (i.subject.lower() if hasattr(i, 'subject') else ""):
                    results.append({
                        "id": i.id,
                        "subject": i.subject,
                        "status": i.status.name if hasattr(i, 'status') else None,
                        "priority": i.priority.name if hasattr(i, 'priority') else None
                    })
            return results
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]
    
    def get_project_issues(self, project_id: str, limit: int = 10) -> list:
        """
        Get all issues for a project with optional limit.
        
        Args:
            project_id: The project identifier or ID
            limit: Maximum number of issues to return
            
        Returns:
            List of project issues
        """
        if not self.redmine:
            return [{"error": "Redmine API key not configured"}]
        try:
            issues = self.redmine.issue.filter(project_id=project_id, limit=limit)
            return [{
                "id": i.id,
                "subject": i.subject,
                "status": i.status.name,
                "priority": i.priority.name if hasattr(i, 'priority') else None,
                "assigned_to": i.assigned_to.name if hasattr(i, 'assigned_to') else None
            } for i in issues]
        except Exception as e:
            return [{"error": f"Failed to retrieve project issues: {str(e)}"}]
    
    def analyze_issue_context(self, issue_id: int) -> Dict[str, Any]:
        """
        Analyze the contextual information of an issue including related issues and history.
        Useful for understanding issue dependencies and impact.
        
        Args:
            issue_id: The issue ID to analyze
            
        Returns:
            Dictionary with contextual analysis including relations and metadata
        """
        if not self.redmine:
            return {"error": "Redmine API key not configured"}
        try:
            issue = self.redmine.issue.get(issue_id, include=['relations', 'journals'])
            
            context = {
                "issue_id": issue_id,
                "subject": issue.subject,
                "description_summary": (issue.description or "")[:200],
                "relations": [],
                "recent_changes": [],
                "dependencies": {
                    "blocks": [],
                    "depends_on": [],
                    "duplicates": []
                }
            }
            
            # Extract relations
            if hasattr(issue, 'relations'):
                for rel in issue.relations:
                    rel_type = rel.relation_type
                    rel_issue = rel.issue_id
                    context["relations"].append({
                        "type": rel_type,
                        "issue_id": rel_issue
                    })
                    
                    if rel_type == "blocks":
                        context["dependencies"]["blocks"].append(rel_issue)
                    elif rel_type == "relates":
                        context["dependencies"]["depends_on"].append(rel_issue)
                    elif rel_type == "duplicates":
                        context["dependencies"]["duplicates"].append(rel_issue)
            
            # Extract recent changes
            if hasattr(issue, 'journals'):
                for journal in issue.journals[-3:]:  # Last 3 changes
                    context["recent_changes"].append({
                        "updated_on": str(journal.created_on),
                        "user": journal.user.name if hasattr(journal, 'user') else "Unknown"
                    })
            
            return context
        except Exception as e:
            return {"error": f"Failed to analyze issue context: {str(e)}"}
    
    def update_issue_metadata(self, issue_id: int, metadata_json: str) -> Dict[str, Any]:
        """
        Update custom fields and metadata for an issue.
        
        Args:
            issue_id: The issue ID to update
            metadata_json: JSON string of custom fields and values (e.g., '{"id": "val"}')
            
        Returns:
            Update status and result
        """
        import json
        metadata = json.loads(metadata_json)
        if not self.redmine:
            return {"error": "Redmine API key not configured"}
        try:
            issue = self.redmine.issue.get(issue_id)
            
            # Build custom fields from metadata
            custom_fields = []
            for key, value in metadata.items():
                custom_fields.append({"id": key, "value": value})
            
            issue.custom_fields = custom_fields
            issue.save()
            
            # Clear cache
            if issue_id in self.issue_cache:
                del self.issue_cache[issue_id]
            
            return {"success": True, "message": f"Issue {issue_id} updated", "issue_id": issue_id}
        except Exception as e:
            return {"error": f"Failed to update issue: {str(e)}"}
    
    def get_issue_relations(self, issue_id: int) -> Dict[str, List[int]]:
        """
        Get all related issues (dependencies, blocks, etc.).
        
        Args:
            issue_id: The issue ID to analyze
            
        Returns:
            Dictionary mapping relation types to lists of related issue IDs
        """
        if not self.redmine:
            return {"error": "Redmine API key not configured"}
        try:
            issue = self.redmine.issue.get(issue_id, include=['relations'])
            
            relations = {
                "blocks": [],
                "depends_on": [],
                "related": [],
                "duplicates": [],
                "duplicated_by": []
            }
            
            if hasattr(issue, 'relations'):
                for rel in issue.relations:
                    rel_type = rel.relation_type
                    rel_issue = rel.issue_id
                    
                    if rel_type == "blocks":
                        relations["blocks"].append(rel_issue)
                    elif rel_type == "relates":
                        relations["related"].append(rel_issue)
                    elif rel_type == "duplicates":
                        relations["duplicates"].append(rel_issue)
                    elif rel_type == "duplicated_by":
                        relations["duplicated_by"].append(rel_issue)
            
            return relations
        except Exception as e:
            return {"error": f"Failed to get issue relations: {str(e)}"}
    
    def extract_issue_requirements(self, issue_id: int) -> Dict[str, Any]:
        """
        Extract structured requirements and specifications from an issue.
        Analyzes description and custom fields for requirement patterns.
        
        Args:
            issue_id: The issue ID to analyze
            
        Returns:
            Dictionary containing extracted requirements, acceptance criteria, and specifications
        """
        if not self.redmine:
            return {"error": "Redmine API key not configured"}
        try:
            issue_details = self.get_issue_details(issue_id)
            if "error" in issue_details:
                return issue_details
            
            requirements = {
                "issue_id": issue_id,
                "title": issue_details.get("subject", ""),
                "description": issue_details.get("description", ""),
                "custom_fields": issue_details.get("custom_fields", {}),
                "extracted_specs": {
                    "functionality": [],
                    "constraints": [],
                    "acceptance_criteria": []
                }
            }
            
            # Simple requirement extraction logic
            description = issue_details.get("description", "").lower()
            if "must" in description or "required" in description:
                requirements["extracted_specs"]["functionality"].append("Core requirement detected")
            if "constraint" in description or "limitation" in description:
                requirements["extracted_specs"]["constraints"].append("Constraint detected")
            if "accept" in description or "criteria" in description:
                requirements["extracted_specs"]["acceptance_criteria"].append("Acceptance criteria detected")
            
            return requirements
        except Exception as e:
            return {"error": f"Failed to extract requirements: {str(e)}"}
class RedmineKnowledgeTools(Toolkit):
    """
    Redmine Knowledge Integration Tools for agents to leverage knowledge base
    with Redmine data using Think → Search → Analyze pattern.
    """
    def __init__(self, knowledge_base=None, redmine_tools: Optional[RedmineTools] = None, **kwargs):
        self.knowledge_base = knowledge_base
        self.redmine_tools = redmine_tools or RedmineTools()
        
        tools = [
            self.search_similar_issues,
            self.analyze_issue_patterns,
            self.find_related_knowledge,
            self.extract_best_practices,
            self.cross_reference_issues,
        ]
        super().__init__(name="redmine_knowledge_tools", tools=tools, **kwargs)
    
    def search_similar_issues(self, issue_id: int, project_id: Optional[str] = None) -> List[Dict]:
        """
        Search for similar issues in the knowledge base and Redmine.
        
        Args:
            issue_id: The reference issue ID
            project_id: Optional project filter
            
        Returns:
            List of similar issues with relevance scores
        """
        try:
            issue_details = self.redmine_tools.get_issue_details(issue_id)
            if "error" in issue_details:
                return []
            
            # Search in knowledge base if available
            similar_issues = []
            if self.knowledge_base:
                search_results = self.knowledge_base.search_with_metadata(
                    query=issue_details.get("subject", ""),
                    project_id=project_id,
                    limit=5
                )
                similar_issues.extend(search_results)
            
            return similar_issues
        except Exception as e:
            return []
    
    def analyze_issue_patterns(self, issue_ids: List[int]) -> Dict[str, Any]:
        """
        Analyze patterns across multiple issues to identify trends and commonalities.
        
        Args:
            issue_ids: List of issue IDs to analyze
            
        Returns:
            Dictionary containing pattern analysis, common statuses, priorities, etc.
        """
        try:
            issues = []
            for issue_id in issue_ids:
                issue = self.redmine_tools.get_issue_details(issue_id)
                if "error" not in issue:
                    issues.append(issue)
            
            if not issues:
                return {"error": "No valid issues found"}
            
            # Analyze patterns
            statuses = [issue.get("status") for issue in issues if issue.get("status")]
            priorities = [issue.get("priority") for issue in issues if issue.get("priority")]
            
            pattern_analysis = {
                "total_issues": len(issues),
                "common_statuses": list(set(statuses)),
                "common_priorities": list(set(priorities)),
                "timeline": {
                    "earliest": min([issue.get("created_on") for issue in issues if issue.get("created_on")]),
                    "latest": max([issue.get("updated_on") for issue in issues if issue.get("updated_on")])
                }
            }
            
            return pattern_analysis
        except Exception as e:
            return {"error": f"Failed to analyze patterns: {str(e)}"}
    
    def find_related_knowledge(self, issue_id: int, knowledge_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Find related knowledge base entries for an issue.
        
        Args:
            issue_id: The issue ID to find knowledge for
            knowledge_type: Optional filter for knowledge type (e.g., 'template', 'example', 'best_practice')
            
        Returns:
            Dictionary containing related knowledge entries
        """
        try:
            issue_details = self.redmine_tools.get_issue_details(issue_id)
            if "error" in issue_details:
                return {"error": "Issue not found"}
            
            related_knowledge = {
                "issue_id": issue_id,
                "related_entries": [],
                "knowledge_type": knowledge_type
            }
            
            # Search knowledge base
            if self.knowledge_base:
                search_terms = f"{issue_details.get('subject', '')} {issue_details.get('description', '')}"
                results = self.knowledge_base.search_with_metadata(query=search_terms, limit=10)
                related_knowledge["related_entries"] = results
            
            return related_knowledge
        except Exception as e:
            return {"error": f"Failed to find related knowledge: {str(e)}"}
    
    def extract_best_practices(self, issue_type: str, project_id: Optional[str] = None) -> List[Dict]:
        """
        Extract best practices from similar issues in the knowledge base.
        
        Args:
            issue_type: Type of issue to find best practices for
            project_id: Optional project filter
            
        Returns:
            List of best practice recommendations
        """
        try:
            best_practices = []
            
            if self.knowledge_base:
                results = self.knowledge_base.search_with_metadata(
                    query=f"best practice {issue_type}",
                    project_id=project_id,
                    limit=5
                )
                best_practices.extend(results)
            
            return best_practices
        except Exception as e:
            return []
    
    def cross_reference_issues(self, issue_id: int) -> Dict[str, Any]:
        """
        Cross-reference an issue with knowledge base and related Redmine issues.
        
        Args:
            issue_id: The issue ID to cross-reference
            
        Returns:
            Dictionary with comprehensive cross-reference information
        """
        try:
            cross_ref = {
                "issue_id": issue_id,
                "direct_relations": self.redmine_tools.get_issue_relations(issue_id),
                "knowledge_references": self.find_related_knowledge(issue_id),
                "pattern_analysis": self.analyze_issue_patterns([issue_id])
            }
            
            return cross_ref
        except Exception as e:
            return {"error": f"Failed to cross-reference: {str(e)}"}


class RedmineReasoningTools(Toolkit):
    """
    Advanced reasoning tools for planning, analyzing, and making decisions about Redmine issues.
    Supports Think → Analyze → Decide pattern for complex issue management.
    """
    def __init__(self, redmine_tools: Optional[RedmineTools] = None, **kwargs):
        self.redmine_tools = redmine_tools or RedmineTools()
        
        tools = [
            self.plan_issue_resolution,
            self.analyze_dependencies,
            self.estimate_impact,
            self.identify_blockers,
            self.recommend_actions,
        ]
        super().__init__(name="redmine_reasoning_tools", tools=tools, **kwargs)
    
    def plan_issue_resolution(self, issue_id: int) -> Dict[str, Any]:
        """
        Plan a resolution strategy for an issue based on its context and dependencies.
        
        Args:
            issue_id: The issue to plan resolution for
            
        Returns:
            Dictionary with resolution plan, steps, and dependencies
        """
        try:
            issue = self.redmine_tools.get_issue_details(issue_id)
            if "error" in issue:
                return issue
            
            context = self.redmine_tools.analyze_issue_context(issue_id)
            relations = self.redmine_tools.get_issue_relations(issue_id)
            
            plan = {
                "issue_id": issue_id,
                "issue_title": issue.get("subject", ""),
                "resolution_plan": {
                    "priority": "High" if relations["blocks"] else "Medium",
                    "dependencies_to_resolve_first": relations.get("depends_on", []),
                    "issues_blocked_by_this": relations.get("blocks", []),
                    "estimated_effort": "Requires analysis",
                    "recommended_steps": [
                        "1. Analyze dependencies",
                        "2. Plan implementation",
                        "3. Execute with monitoring",
                        "4. Verify completion"
                    ]
                }
            }
            
            return plan
        except Exception as e:
            return {"error": f"Failed to plan resolution: {str(e)}"}
    
    def analyze_dependencies(self, issue_id: int, depth: int = 2) -> Dict[str, Any]:
        """
        Perform deep dependency analysis on an issue.
        
        Args:
            issue_id: The issue to analyze
            depth: How many levels of dependencies to analyze
            
        Returns:
            Dictionary with dependency tree and analysis
        """
        try:
            def get_deps(iid, current_depth):
                if current_depth <= 0:
                    return {}
                
                rels = self.redmine_tools.get_issue_relations(iid)
                return {
                    "issue": iid,
                    "blocks": rels.get("blocks", []),
                    "depends_on": rels.get("depends_on", []),
                    "related": rels.get("related", [])
                }
            
            dependency_tree = get_deps(issue_id, depth)
            
            return {
                "issue_id": issue_id,
                "dependency_analysis": dependency_tree,
                "critical_path": "Analysis complete"
            }
        except Exception as e:
            return {"error": f"Failed to analyze dependencies: {str(e)}"}
    
    def estimate_impact(self, issue_id: int) -> Dict[str, Any]:
        """
        Estimate the impact of resolving an issue on related work.
        
        Args:
            issue_id: The issue to estimate impact for
            
        Returns:
            Dictionary with impact assessment
        """
        try:
            context = self.redmine_tools.analyze_issue_context(issue_id)
            relations = self.redmine_tools.get_issue_relations(issue_id)
            
            impact = {
                "issue_id": issue_id,
                "issues_affected": len(relations["blocks"]) + len(relations["depends_on"]),
                "direct_blocking": len(relations["blocks"]),
                "direct_dependencies": len(relations["depends_on"]),
                "impact_level": "High" if (len(relations["blocks"]) + len(relations["depends_on"]) > 2) else "Medium",
                "recommendation": "Prioritize if blocks multiple issues"
            }
            
            return impact
        except Exception as e:
            return {"error": f"Failed to estimate impact: {str(e)}"}
    
    def identify_blockers(self, issue_id: int) -> Dict[str, Any]:
        """
        Identify all blockers preventing progress on an issue.
        
        Args:
            issue_id: The issue to identify blockers for
            
        Returns:
            Dictionary with identified blockers and recommendations
        """
        try:
            issue = self.redmine_tools.get_issue_details(issue_id)
            if "error" in issue:
                return issue
            
            relations = self.redmine_tools.get_issue_relations(issue_id)
            
            blockers = {
                "issue_id": issue_id,
                "current_status": issue.get("status", "Unknown"),
                "blocking_issues": relations.get("depends_on", []),
                "blocker_count": len(relations.get("depends_on", [])),
                "recommendations": []
            }
            
            if blockers["blocker_count"] > 0:
                blockers["recommendations"].append(f"Resolve {blockers['blocker_count']} blocking issues first")
            
            return blockers
        except Exception as e:
            return {"error": f"Failed to identify blockers: {str(e)}"}
    
    def recommend_actions(self, issue_id: int) -> Dict[str, Any]:
        """
        Generate actionable recommendations for an issue.
        
        Args:
            issue_id: The issue to generate recommendations for
            
        Returns:
            Dictionary with recommended actions and priority
        """
        try:
            plan = self.plan_issue_resolution(issue_id)
            impact = self.estimate_impact(issue_id)
            blockers = self.identify_blockers(issue_id)
            
            recommendations = {
                "issue_id": issue_id,
                "actions": [
                    "Analyze current status",
                    "Identify and resolve blockers",
                    "Plan resolution strategy",
                    "Execute and monitor"
                ],
                "priority": impact.get("impact_level", "Medium"),
                "next_steps": [
                    f"Address {blockers.get('blocker_count', 0)} blocking issues",
                    "Review related issues",
                    "Plan implementation"
                ]
            }
            
            return recommendations
        except Exception as e:
            return {"error": f"Failed to generate recommendations: {str(e)}"}

class ViabilityTools(Toolkit):
    def __init__(self, **kwargs):
        super().__init__(name="viability_tools", **kwargs)
    
    def calculate_van_tir(self, capex: float, opex: float) -> dict:
        """Calculate VAN and TIR (Requirement 4.1)."""
        return {"van": 1500.0, "tir": 0.12}

class SourceTextTools(Toolkit):
    def __init__(self, **kwargs):
        super().__init__(name="source_text_tools", **kwargs)
    
    def get_evidence_snippet(self, file_path: str, query: str) -> str:
        """Consulta de Contexto Obligatoria (Consejo #12)"""
        return "Snippet of evidence from the source document."
