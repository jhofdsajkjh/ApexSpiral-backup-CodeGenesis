"""
CodeGenesis Φ_code 完整实现
核心公式真实代码落地
"""

from dataclasses import dataclass
from typing import Optional
import math


@dataclass
class PhiCodeInput:
    """Φ_code输入参数"""
    # 分子参数（质量提升因子）
    E_std: float      # 工程标准化度 (0~1)
    Psi_logic: float  # 逻辑连贯系数 (0~1)
    Theta_check: float # 校验覆盖率 (0~1) - 师父指正：Θ=校验覆盖率
    Gamma_task: float  # 任务分解度 (0~1)
    Omega_aware: float # 上下文感知度 (0~1)
    alpha_best: float  # 最优路径系数 (0~1)
    
    # 分母参数（质量衰减因子）
    R_dup: float      # 代码重复率 (>0)
    B_bug: float      # 缺陷密度 (>0)
    C_chaos: float    # 混沌度 (>0)
    delta_ctx: float   # 短上下文衰减 (>0)
    mu_loss: float     # 记忆遗忘率 (>0)


class PhiCodeCalculator:
    """Φ_code公式计算器"""
    
    # 符号统一规范（依据APEX_UNIFIED_NOTATION.md）
    SYMBOLS = {
        'E_std': '工程标准化度',
        'Psi_logic': '逻辑连贯系数', 
        'Theta_check': '校验覆盖率',  # Θ=校验，不是时间衰减
        'Gamma_task': '任务分解度',
        'Omega_aware': '上下文感知度',
        'alpha_best': '最优路径系数',
        'R_dup': '代码重复率',
        'B_bug': '缺陷密度',
        'C_chaos': '混沌度',
        'delta_ctx': '短上下文衰减',
        'mu_loss': '记忆遗忘率'
    }
    
    def __init__(self):
        self.last_result: Optional[float] = None
        self.history: list = []
    
    def calculate(self, inp: PhiCodeInput) -> dict:
        """
        核心公式: Φ_code = (E_std × Ψ_logic × Θ_check × Γ_task × Ω_aware × α_best) / (R_dup × B_bug × C_chaos × δ_ctx × μ_loss)
        """
        # 参数校验
        if any(v <= 0 for v in [inp.R_dup, inp.B_bug, inp.C_chaos, inp.delta_ctx, inp.mu_loss]):
            return {
                'phi_code': float('inf'),
                'valid': False,
                'error': '分母参数必须大于0'
            }
        
        # 分子计算
        numerator = (inp.E_std * inp.Psi_logic * inp.Theta_check * 
                     inp.Gamma_task * inp.Omega_aware * inp.alpha_best)
        
        # 分母计算
        denominator = (inp.R_dup * inp.B_bug * inp.C_chaos * 
                       inp.delta_ctx * inp.mu_loss)
        
        # Φ_code计算
        phi_code = numerator / denominator
        
        # 记录历史
        self.last_result = phi_code
        self.history.append({
            'phi_code': phi_code,
            'numerator': numerator,
            'denominator': denominator
        })
        
        return {
            'phi_code': phi_code,
            'valid': True,
            'numerator': numerator,
            'denominator': denominator,
            'description': self._format_description(inp)
        }
    
    def _format_description(self, inp: PhiCodeInput) -> str:
        """生成描述字符串"""
        return (f"Φ_code = ({inp.E_std}×{inp.Psi_logic}×{inp.Theta_check}×"
                f"{inp.Gamma_task}×{inp.Omega_aware}×{inp.alpha_best}) / "
                f"({inp.R_dup}×{inp.B_bug}×{inp.C_chaos}×{inp.delta_ctx}×{inp.mu_loss})")
    
    def quick_score(self, dup_rate: float, bug_rate: float, chaos: float,
                    ctx_loss: float, info_loss: float) -> float:
        """
        快速评分（简化版）
        适用于快速估算
        """
        # 假设分子参数都为0.9
        numerator = 0.9 ** 6  # ≈0.53
        denominator = dup_rate * bug_rate * chaos * ctx_loss * info_loss
        
        if denominator <= 0:
            return float('inf')
        
        return numerator / denominator


# 全局计算器实例
calculator = PhiCodeCalculator()
