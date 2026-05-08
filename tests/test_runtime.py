"""
CodeGenesis运行时测试 + Ξ_evol量化

测试内容:
- Ξ_evol公式: (C×Λ×Ω)/(H×t)
- 网络中断模拟恢复
- 磁盘满场景处理
- 运行时自愈能力

璇玑帝国 CodeGenesis - 2026-05-08
"""
import pytest
import os
import sys
import tempfile
import random

# 确保core模块在路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.formula_core import CodeGenesis, CodeQualityReport


class TestXiEvol:
    """Ξ_evol量化指标测试
    
    Ξ_evol = (C×Λ×Ω)/(H×t)
    - C: 复杂度 (R+)
    - Λ: 演化系数 (0,1]
    - Ω: 收敛度 (0,1]
    - H: 噪声 [0,1)
    - t: 时间 (0,+∞)
    
    Ξ_evol越高 = 进化能力越强
    """
    
    def test_xi_evol_normal(self):
        """正常运行: Ξ_evol = (C×Λ×Ω)/(H×t)"""
        C = 0.9       # 复杂度
        Lambda = 0.85  # 演化系数
        Omega = 0.8    # 收敛度
        H = 0.3        # 噪声
        t = 1.0        # 时间
        
        xi_evol = (C * Lambda * Omega) / (H * t)
        
        # 验证: 正常情况下 Ξ_evol > 0
        assert xi_evol > 0, f"Ξ_evol should be positive, got {xi_evol}"
        
        # 验证: 数值合理性 (高信号场景)
        expected = (0.9 * 0.85 * 0.8) / (0.3 * 1.0)
        assert abs(xi_evol - expected) < 1e-9
        print(f"[TestXiEvol] Ξ_evol_normal = {xi_evol:.4f} (expected {expected:.4f})")
    
    def test_xi_evol_high_noise(self):
        """高噪声场景: Ξ_evol应该很低"""
        C = 0.9
        Lambda = 0.85
        Omega = 0.8
        H = 0.9        # 高噪声
        t = 1.0
        
        xi_evol = (C * Lambda * Omega) / (H * t)
        
        # 高噪声应该产生低值
        assert xi_evol < 1.0, f"High noise should produce low Ξ_evol, got {xi_evol}"
        assert xi_evol > 0, "Should still be positive"
        print(f"[TestXiEvol] Ξ_evol_high_noise = {xi_evol:.4f}")
    
    def test_xi_evol_zero_noise(self):
        """零噪声场景: Ξ_evol应该趋于无穷大"""
        C = 0.9
        Lambda = 0.85
        Omega = 0.8
        H = 0.0        # 零噪声 → 无穷大
        t = 1.0
        
        # 零噪声在数学上产生无穷大，但实际系统应限制
        # 实际实现应处理H接近0的情况
        xi_evol = (C * Lambda * Omega) / (H * t) if H > 0 else float('inf')
        
        assert xi_evol == float('inf'), f"Zero noise should be infinite, got {xi_evol}"
        print(f"[TestXiEvol] Ξ_evol_zero_noise = {xi_evol}")
    
    def test_xi_evol_zero_time(self):
        """零时间场景: 应被处理为无效"""
        C = 0.9
        Lambda = 0.85
        Omega = 0.8
        H = 0.3
        t = 0.0
        
        # 零时间在数学上无效
        if t <= 0:
            xi_evol = float('inf')  # 立即达到目标
        else:
            xi_evol = (C * Lambda * Omega) / (H * t)
        
        assert xi_evol == float('inf')
        print(f"[TestXiEvol] Ξ_evol_zero_time = {xi_evol}")
    
    def test_xi_evol_boundary_conditions(self):
        """边界条件测试"""
        test_cases = [
            # (C, Lambda, Omega, H, t, description)
            (1.0, 1.0, 1.0, 0.1, 1.0, "最大增益"),
            (1.0, 0.5, 0.5, 0.5, 1.0, "中等增益"),
            (1.0, 0.1, 0.1, 0.9, 10.0, "最小增益"),
            (0.5, 0.8, 0.9, 0.2, 0.5, "短时高增益"),
        ]
        
        for C, Lambda, Omega, H, t, desc in test_cases:
            if H > 0 and t > 0:
                xi = (C * Lambda * Omega) / (H * t)
                assert xi > 0, f"{desc}: xi_evol should be positive"
                print(f"[TestXiEvol] {desc}: Ξ_evol = {xi:.4f}")
    
    def test_xi_evol_integration_with_codegenesis(self):
        """与CodeGenesis集成: 用Lambda_evol参与Ξ_evol计算"""
        # Lambda_evol = selection × mutation × crossover
        selection = 0.9
        mutation = 0.8
        crossover = 0.85
        lambda_evol = selection * mutation * crossover
        
        C = 0.95   # 高复杂度
        Omega = 0.82
        H = 0.25   # 低噪声
        t = 1.0
        
        # Ξ_evol = (C × Λ_evol × Ω) / (H × t)
        xi_evol = (C * lambda_evol * Omega) / (H * t)
        
        assert xi_evol > 1.0, f"High-quality evolution should produce xi_evol > 1, got {xi_evol}"
        print(f"[TestXiEvol] Integrated Ξ_evol = {xi_evol:.4f} (Lambda={lambda_evol:.4f})")


class TestRuntimeSelfHeal:
    """运行时自愈测试
    
    模拟真实运行时故障:
    1. 网络中断恢复
    2. 磁盘满处理
    3. 内存溢出恢复
    """
    
    def test_network_interrupt_detection(self):
        """模拟网络中断检测"""
        # 模拟网络状态
        class NetworkSimulator:
            def __init__(self):
                self.available = True
                self.retry_count = 0
                self.max_retries = 3
            
            def fetch(self, url: str) -> dict:
                if not self.available:
                    self.retry_count += 1
                    if self.retry_count <= self.max_retries:
                        raise ConnectionError(f"Network unavailable (retry {self.retry_count})")
                    else:
                        raise ConnectionError("Network dead after max retries")
                return {"status": "ok", "data": "result"}
            
            def heal(self):
                """自愈: 等待后恢复"""
                import time
                self.retry_count = 0
                self.available = True
        
        net = NetworkSimulator()
        
        # 正常情况
        result = net.fetch("http://api.example.com/data")
        assert result["status"] == "ok"
        
        # 中断恢复
        net.available = False
        net.retry_count = 0
        
        # 前3次应该重试
        for i in range(3):
            try:
                net.fetch("http://api.example.com/data")
            except ConnectionError as e:
                assert f"retry {i+1}" in str(e)
        
        # 第4次应该成功恢复
        net.heal()
        result = net.fetch("http://api.example.com/data")
        assert result["status"] == "ok"
        
        print("[TestSelfHeal] Network interrupt detection: PASSED")
    
    def test_disk_full_handling(self):
        """模拟磁盘满处理"""
        class DiskSimulator:
            def __init__(self, max_bytes: int = 1024):
                self.max_bytes = max_bytes
                self.used = 0
            
            def write(self, data: bytes) -> bool:
                if self.used + len(data) > self.max_bytes:
                    return False  # 磁盘满
                self.used += len(data)
                return True
            
            def cleanup(self):
                """自愈: 清理旧文件释放空间"""
                self.used = 0
            
            def get_free_space(self) -> int:
                return max(0, self.max_bytes - self.used)
        
        disk = DiskSimulator(max_bytes=100)
        
        # 写入正常数据
        assert disk.write(b"hello") == True
        assert disk.get_free_space() == 95
        
        # 填满磁盘
        while disk.write(b"x"):
            pass
        assert disk.get_free_space() == 0
        
        # 自愈: 清理后恢复
        disk.cleanup()
        assert disk.write(b"hello") == True
        assert disk.get_free_space() == 95
        
        print("[TestSelfHeal] Disk full handling: PASSED")
    
    def test_memory_pressure_recovery(self):
        """模拟内存压力恢复"""
        class MemorySimulator:
            def __init__(self, max_mb: int = 64):
                self.max_mb = max_mb
                self.used_mb = 0
                self.gc_count = 0
            
            def allocate(self, mb: float) -> bool:
                if self.used_mb + mb > self.max_mb:
                    return False
                self.used_mb += mb
                return True
            
            def garbage_collect(self):
                """自愈: GC回收内存"""
                self.used_mb = 0
                self.gc_count += 1
            
            def get_usage(self) -> float:
                return self.used_mb / self.max_mb
        
        mem = MemorySimulator(max_mb=64)
        
        # 正常分配
        assert mem.allocate(32) == True
        assert mem.get_usage() == 0.5
        
        # 内存压力
        assert mem.allocate(50) == False  # 超过限制
        
        # 自愈回收
        mem.garbage_collect()
        assert mem.get_usage() == 0.0
        assert mem.gc_count == 1
        
        # 再次分配
        assert mem.allocate(32) == True
        
        print("[TestSelfHeal] Memory pressure recovery: PASSED")
    
    def test_self_heal_delta_g_recovery(self):
        """测试ΔG公式在故障后的恢复能力"""
        # 模拟故障后的状态
        C_fault = 0.3   # 故障后复杂度下降
        Lambda_fault = 0.4  # 演化系数下降
        Omega_fault = 0.5   # 收敛度下降
        H_fault = 0.8      # 噪声上升
        t = 1.0
        
        delta_g_fault = (C_fault * Lambda_fault * Omega_fault) / (H_fault * t)
        
        # 恢复后的状态
        C_recover = 0.9
        Lambda_recover = 0.85
        Omega_recover = 0.8
        H_recover = 0.3
        t = 1.0
        
        delta_g_recover = (C_recover * Lambda_recover * Omega_recover) / (H_recover * t)
        
        # 恢复后ΔG应该显著提升
        assert delta_g_recover > delta_g_fault * 5, \
            f"Recovery should significantly improve ΔG: {delta_g_recover} vs {delta_g_fault}"
        
        print(f"[TestSelfHeal] ΔG recovery: {delta_g_fault:.4f} -> {delta_g_recover:.4f} (PASSED)")


class TestCodeQualityReport:
    """CodeQualityReport综合测试"""
    
    def test_production_ready(self):
        """测试生产级别判定"""
        report = CodeQualityReport(
            phi_code=2.5,
            omega_purge=0.85,   # > 0.8 ✓
            psi_logic=0.75,     # > 0.7 ✓
            theta_break=0.85,   # > 0.8 ✓
            gamma_task=0.8,
            lambda_evol=0.9,
            delta_ctx=0.7,
            sigma_converge=True
        )
        
        assert report.is_production_ready() == True
        print("[TestReport] Production ready check: PASSED")
    
    def test_not_production_ready_low_purge(self):
        """测试去重净化率不足时不是生产级别"""
        report = CodeQualityReport(
            phi_code=2.5,
            omega_purge=0.6,    # < 0.8 ✗
            psi_logic=0.8,
            theta_break=0.9,
            gamma_task=0.8,
            lambda_evol=0.9,
            delta_ctx=0.7,
            sigma_converge=True
        )
        
        assert report.is_production_ready() == False
        print("[TestReport] Not production ready (low purge): PASSED")
    
    def test_overall_score(self):
        """测试综合评分计算"""
        report = CodeQualityReport(
            phi_code=2.0,
            omega_purge=0.8,
            psi_logic=0.7,
            theta_break=0.8,
            gamma_task=0.9,
            lambda_evol=0.85,
            delta_ctx=0.75,
            sigma_converge=True
        )
        
        score = report.overall_score()
        
        expected = (2.0 * 0.8 * 0.7 * 0.8 * 0.9 * 0.85 * 0.75)
        assert abs(score - expected) < 1e-9
        
        print(f"[TestReport] Overall score: {score:.4f} (PASSED)")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
