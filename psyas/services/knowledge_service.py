# -*- coding: utf-8 -*-
"""心理学知识库服务 (KnowledgeService) - 提供专业心理学知识支持."""
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class KnowledgeMatch:
    """知识匹配结果."""

    framework: str
    confidence: float
    response_template: str
    follow_up_questions: List[str]
    techniques: List[Dict]
    immediate_response: str


class KnowledgeService:
    """心理学知识库服务类，负责匹配心理学知识并提供专业建议."""

    def __init__(self):
        """初始化知识库服务."""
        self.frameworks = self._load_frameworks()
        self.issues = self._load_issues()

        # 危机关键词检测
        self.crisis_keywords = [
            "自杀",
            "伤害自己",
            "想死",
            "结束生命",
            "轻生",
            "自残",
            "不想活",
            "活着没意思",
        ]

    def _load_frameworks(self) -> Dict:
        """加载心理学框架数据."""
        frameworks_path = os.path.join(
            os.path.dirname(__file__), "../data/psychology_frameworks.json"
        )
        try:
            with open(frameworks_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"警告：找不到框架文件 {frameworks_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"警告：框架文件格式错误 {e}")
            return {}

    def _load_issues(self) -> Dict:
        """加载心理问题分类数据."""
        issues_path = os.path.join(
            os.path.dirname(__file__), "../data/psychological_issues.json"
        )
        try:
            with open(issues_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"警告：找不到问题分类文件 {issues_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"警告：问题分类文件格式错误 {e}")
            return {}

    def analyze_user_input(
        self, user_input: str, detected_emotion: str = None
    ) -> Optional[KnowledgeMatch]:
        """
        分析用户输入并匹配相关心理学知识.

        Args:
            user_input: 用户输入的文本
            detected_emotion: 已检测到的情绪（来自现有服务）

        Returns:
            KnowledgeMatch: 匹配结果，如果没有匹配则返回None
        """

        # 1. 危机检测
        if self._is_crisis_situation(user_input):
            return self._get_crisis_response()

        # 2. 匹配心理问题
        matched_issue = self._match_psychological_issue(user_input, detected_emotion)
        if not matched_issue:
            return self._get_default_response(detected_emotion)

        # 3. 获取建议的框架
        framework_name = matched_issue.get("suggested_framework")
        if framework_name not in self.frameworks:
            return self._get_default_response(detected_emotion)

        framework = self.frameworks[framework_name]

        # 4. 计算匹配度
        confidence = self._calculate_confidence(user_input, matched_issue)

        # 5. 选择合适的回应模板
        response_template = self._select_response_template(matched_issue, framework)

        # 6. 获取立即回应
        immediate_response = self._get_immediate_response(matched_issue, user_input)

        # 7. 生成后续问题
        follow_up_questions = matched_issue.get("follow_up_questions", [])

        # 8. 获取干预技巧
        techniques = self._get_relevant_techniques(framework, detected_emotion or "")

        return KnowledgeMatch(
            framework=framework_name,
            confidence=confidence,
            response_template=response_template,
            follow_up_questions=follow_up_questions,
            techniques=techniques,
            immediate_response=immediate_response,
        )

    def _is_crisis_situation(self, user_input: str) -> bool:
        """检测是否为危机情况."""
        user_input_lower = user_input.lower()

        # 直接危机关键词
        direct_crisis = [
            "自杀",
            "伤害自己",
            "想死",
            "结束生命",
            "轻生",
            "自残",
            "不想活",
            "活着没意思",
        ]

        # 间接危机组合词
        pain_words = ["痛苦", "难受", "煎熬", "折磨"]
        life_words = ["活着", "人生", "生活", "存在"]
        end_words = ["结束", "解脱", "逃离", "放弃"]

        # 检查直接危机关键词
        if any(keyword in user_input_lower for keyword in direct_crisis):
            return True

        # 检查间接危机组合：生活相关词 + 痛苦词 + 结束词
        has_life = any(word in user_input_lower for word in life_words)
        has_pain = any(word in user_input_lower for word in pain_words)
        has_end = any(word in user_input_lower for word in end_words)

        # 如果同时包含生活词、痛苦词和结束词，判定为危机
        if has_life and has_pain and has_end:
            return True

        return False

    def _get_crisis_response(self) -> KnowledgeMatch:
        """获取危机情况的回应."""
        return KnowledgeMatch(
            framework="危机干预",
            confidence=1.0,
            response_template="我很担心你现在的状态。你的生命很珍贵，现在需要专业帮助。",
            follow_up_questions=[
                "你现在是否安全？",
                "身边有可以信任的人吗？",
                "愿意联系专业的心理危机热线吗？",
            ],
            techniques=[
                {
                    "name": "立即转介",
                    "description": "联系专业心理危机干预服务",
                    "example": "全国心理危机干预热线：400-161-9995",
                }
            ],
            immediate_response="我很关心你的安全。如果你有自伤的想法，请立即联系专业帮助或拨打心理危机热线400-161-9995。",
        )

    def _match_psychological_issue(
        self, user_input: str, detected_emotion: str = None
    ) -> Optional[Dict]:
        """
        匹配心理问题类型.

        优先匹配顺序：
        1. 特殊组合规则（工作+焦虑、分手+抑郁等）
        2. 问题类（具体问题领域）
        3. 情绪类（情绪状态）
        """
        # 检查特殊组合规则
        special_match = self._check_special_combinations(user_input)
        if special_match:
            return special_match

        # 标准匹配流程
        return self._standard_issue_matching(user_input, detected_emotion)

    def _check_special_combinations(self, user_input: str) -> Optional[Dict]:
        """检查特殊组合规则."""
        user_input_lower = user_input.lower()

        # 特殊组合规则：工作压力+焦虑情绪 -> 正念疗法
        work_keywords = ["工作", "上班", "职场"]
        anxiety_keywords = ["焦虑", "担心", "紧张"]

        if any(kw in user_input_lower for kw in work_keywords) and any(
            kw in user_input_lower for kw in anxiety_keywords
        ):
            return self._create_modified_issue_data("焦虑", "正念疗法")

        # 特殊组合规则：分手+抑郁情绪 -> CBT
        relationship_keywords = ["分手", "男朋友", "女朋友", "恋人"]
        depression_keywords = ["难过", "绝望", "沮丧", "抑郁"]

        if any(kw in user_input_lower for kw in relationship_keywords) and any(
            kw in user_input_lower for kw in depression_keywords
        ):
            return self._create_modified_issue_data("抑郁", "CBT")

        return None

    def _create_modified_issue_data(
        self, emotion_type: str, framework: str
    ) -> Optional[Dict]:
        """创建修改过的问题数据."""
        issue_data = self.issues.get("情绪类", {}).get(emotion_type, {})
        if issue_data:
            modified_data = issue_data.copy()
            modified_data["suggested_framework"] = framework
            return modified_data
        return None

    def _standard_issue_matching(
        self, user_input: str, detected_emotion: str = None
    ) -> Optional[Dict]:
        """标准问题匹配流程."""
        user_input_lower = user_input.lower()

        # 优先匹配问题类
        issue_match = self._match_issue_category(user_input_lower, "问题类")
        if issue_match:
            return issue_match

        # 其次匹配情绪类
        emotion_match = self._match_issue_category(user_input_lower, "情绪类")
        if emotion_match:
            return emotion_match

        # 如果有检测到的情绪，尝试匹配
        if detected_emotion:
            emotion_data = self.issues.get("情绪类", {}).get(detected_emotion)
            if emotion_data:
                return emotion_data

        return None

    def _match_issue_category(
        self, user_input_lower: str, category_name: str
    ) -> Optional[Dict]:
        """匹配特定类别的问题."""
        category_data = self.issues.get(category_name, {})
        for issue_name, issue_data in category_data.items():
            keywords = issue_data.get("keywords", [])
            for keyword in keywords:
                if keyword in user_input_lower:
                    return issue_data
        return None

    def _calculate_confidence(self, user_input: str, issue_data: Dict) -> float:
        """计算匹配置信度."""
        keywords = issue_data.get("keywords", [])
        if not keywords:
            return 0.0

        matched_keywords = 0
        user_input_lower = user_input.lower()

        for keyword in keywords:
            if keyword in user_input_lower:
                matched_keywords += 1

        confidence = matched_keywords / len(keywords)

        # 根据文本长度调整置信度
        if len(user_input) > 20:
            confidence += 0.1  # 更详细的描述增加置信度

        return min(confidence, 1.0)

    def _select_response_template(self, issue_data: Dict, framework: Dict) -> str:
        """选择合适的回应模板."""

        # 优先使用框架特定的模板
        framework_responses = framework.get("response_templates", [])
        if framework_responses:
            return framework_responses[0]

        # 备选：使用问题特定的模板
        immediate_responses = issue_data.get("immediate_responses", [])
        if immediate_responses:
            return immediate_responses[0]

        # 兜底模板
        return "我理解你现在的感受，这确实不容易。能告诉我更多关于这个情况的细节吗？"

    def _get_immediate_response(self, issue_data: Dict, user_input: str) -> str:
        """获取立即回应."""
        immediate_responses = issue_data.get("immediate_responses", [])
        if immediate_responses:
            return immediate_responses[0]

        return "我理解你的感受，让我们一起来看看这个情况。"

    def _get_relevant_techniques(self, framework: Dict, emotion: str) -> List[Dict]:
        """获取相关的干预技巧."""
        techniques = framework.get("intervention_techniques", [])

        # 过滤出适用于当前情绪的技巧
        relevant_techniques = []
        for technique in techniques:
            applicable_when = technique.get("applicable_when", [])
            if not applicable_when or emotion in applicable_when:
                relevant_techniques.append(technique)

        # 限制返回数量
        return relevant_techniques[:2]

    def _get_default_response(self, detected_emotion: str = None) -> KnowledgeMatch:
        """获取默认回应."""
        if detected_emotion and detected_emotion != "中性":
            framework_name = self._get_default_framework_for_emotion(detected_emotion)
            framework = self.frameworks.get(framework_name, {})

            return KnowledgeMatch(
                framework=framework_name,
                confidence=0.3,
                response_template=f"我感受到你的{detected_emotion}，这是很正常的情绪。",
                follow_up_questions=[
                    "能告诉我更多关于这种感受吗？",
                    "这种情况持续多长时间了？",
                ],
                techniques=self._get_relevant_techniques(framework, detected_emotion),
                immediate_response=f"我理解你现在感到{detected_emotion}，让我们一起来看看。",
            )

        return KnowledgeMatch(
            framework="通用支持",
            confidence=0.2,
            response_template="我在这里倾听你，你想和我分享什么？",
            follow_up_questions=[
                "能具体说说发生了什么吗？",
                "这件事对你来说意味着什么？",
            ],
            techniques=[],
            immediate_response="我在这里倾听你，你可以和我分享任何感受。",
        )

    def _get_default_framework_for_emotion(self, emotion: str) -> str:
        """根据情绪获取默认框架."""
        emotion_framework_map = {
            "焦虑": "正念疗法",
            "抑郁": "CBT",
            "愤怒": "正念疗法",
            "压力": "正念疗法",
            "快乐": "积极心理学",
            "孤独": "人际关系疗法",
        }
        return emotion_framework_map.get(emotion, "CBT")

    def get_framework_info(self, framework_name: str) -> Optional[Dict]:
        """获取特定框架的详细信息."""
        return self.frameworks.get(framework_name)

    def suggest_techniques(self, framework_name: str, emotion: str = "") -> List[Dict]:
        """根据框架和情绪推荐具体技巧."""
        framework = self.frameworks.get(framework_name)
        if not framework:
            return []

        return self._get_relevant_techniques(framework, emotion)

    def enhance_response_with_knowledge(
        self, base_response: str, user_input: str, detected_emotion: str = None
    ) -> str:
        """
        使用知识库增强现有的回应.

        这个方法可以与现有的ConversationService集成，
        在生成基础回应后进一步增强。
        """
        knowledge_match = self.analyze_user_input(user_input, detected_emotion)

        if not knowledge_match or knowledge_match.confidence < 0.3:
            return base_response

        # 结合知识库的专业建议
        enhanced_response = knowledge_match.immediate_response

        # 添加后续引导问题
        if knowledge_match.follow_up_questions:
            follow_up = knowledge_match.follow_up_questions[0]
            enhanced_response += f" {follow_up}"

        return enhanced_response

    def get_safety_guidelines(self) -> Dict:
        """获取安全使用指南."""
        return {
            "disclaimer": "本系统仅提供心理健康信息支持，不构成专业医疗建议",
            "crisis_hotline": "心理危机干预热线：400-161-9995",
            "refer_to_professional": [
                "持续的抑郁或焦虑症状",
                "自伤或自杀想法",
                "严重的人际关系问题",
                "创伤后应激反应",
            ],
            "boundaries": [
                "不进行心理诊断",
                "不提供药物建议",
                "不处理急性危机情况",
                "不替代专业治疗",
            ],
        }
