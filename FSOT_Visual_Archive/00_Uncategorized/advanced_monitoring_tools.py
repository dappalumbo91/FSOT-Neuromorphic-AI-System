#!/usr/bin/env python3
"""
FSOT System Advanced Monitoring & Automation Tools
=================================================
Real-time monitoring, performance profiling, and automated management.
"""

import os as _os
from pathlib import Path as _Path

_REPO_ROOT = _Path(__file__).resolve().parents[2]


import psutil
import time
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import logging
import sys
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FSATSystemMonitor:
    """Real-time system monitoring for FSOT AI"""
    
    def __init__(self):
        self.monitoring = False
        self.metrics_history: List[Dict[str, Any]] = []
        self.alerts: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
        
    def start_monitoring(self, duration_minutes: int = 5):
        """Start system monitoring for specified duration"""
        self.monitoring = True
        self.start_time = datetime.now()
        
        logger.info(f"🔍 Starting system monitoring for {duration_minutes} minutes...")
        
        monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(duration_minutes,), 
            daemon=True
        )
        monitor_thread.start()
        
        return monitor_thread
    
    def _monitor_loop(self, duration_minutes: int):
        """Main monitoring loop"""
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        
        while self.monitoring and datetime.now() < end_time:
            try:
                metrics = self._collect_metrics()
                self.metrics_history.append(metrics)
                
                # Check for alerts
                self._check_alerts(metrics)
                
                # Log every 30 seconds
                if len(self.metrics_history) % 6 == 0:  # Every 6th measurement (30 seconds)
                    self._log_status(metrics)
                
                time.sleep(5)  # Collect metrics every 5 seconds
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(10)
        
        self.monitoring = False
        self._generate_report()
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system metrics"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'cores': psutil.cpu_count(),
                'frequency': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            'memory': {
                'percent': psutil.virtual_memory().percent,
                'available_gb': round(psutil.virtual_memory().available / (1024**3), 2),
                'used_gb': round(psutil.virtual_memory().used / (1024**3), 2)
            },
            'disk': {
                'percent': psutil.disk_usage('/').percent,
                'free_gb': round(psutil.disk_usage('/').free / (1024**3), 2)
            },
            'network': {
                'bytes_sent': getattr(psutil.net_io_counters(), 'bytes_sent', 0) if psutil.net_io_counters() else 0,
                'bytes_recv': getattr(psutil.net_io_counters(), 'bytes_recv', 0) if psutil.net_io_counters() else 0
            },
            'processes': {
                'total': len(psutil.pids()),
                'python_processes': self._count_python_processes()
            }
        }
    
    def _count_python_processes(self) -> int:
        """Safely count Python processes"""
        count = 0
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.name().lower() if hasattr(proc, 'name') else ''
                    if 'python' in name:
                        count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                    continue
        except Exception:
            pass
        return count
    
    def _check_alerts(self, metrics: Dict[str, Any]):
        """Check for performance alerts"""
        alerts = []
        
        # CPU alerts
        if metrics['cpu']['percent'] > 90:
            alerts.append({'type': 'HIGH_CPU', 'value': metrics['cpu']['percent'], 'threshold': 90})
        
        # Memory alerts
        if metrics['memory']['percent'] > 85:
            alerts.append({'type': 'HIGH_MEMORY', 'value': metrics['memory']['percent'], 'threshold': 85})
        
        # Disk alerts
        if metrics['disk']['percent'] > 90:
            alerts.append({'type': 'LOW_DISK', 'value': metrics['disk']['percent'], 'threshold': 90})
        
        if alerts:
            self.alerts.extend(alerts)
            for alert in alerts:
                logger.warning(f"🚨 ALERT: {alert['type']} - {alert['value']}% (threshold: {alert['threshold']}%)")
    
    def _log_status(self, metrics: Dict[str, Any]):
        """Log current system status"""
        logger.info(f"📊 CPU: {metrics['cpu']['percent']:.1f}% | "
                   f"RAM: {metrics['memory']['percent']:.1f}% | "
                   f"Disk: {metrics['disk']['percent']:.1f}% | "
                   f"Processes: {metrics['processes']['total']}")
    
    def _generate_report(self):
        """Generate monitoring report"""
        if not self.metrics_history:
            return
        
        # Calculate averages
        avg_cpu = sum(m['cpu']['percent'] for m in self.metrics_history) / len(self.metrics_history)
        avg_memory = sum(m['memory']['percent'] for m in self.metrics_history) / len(self.metrics_history)
        max_cpu = max(m['cpu']['percent'] for m in self.metrics_history)
        max_memory = max(m['memory']['percent'] for m in self.metrics_history)
        
        report = {
            'monitoring_period': {
                'start': self.start_time.isoformat() if self.start_time else datetime.now().isoformat(),
                'end': datetime.now().isoformat(),
                'duration_minutes': (datetime.now() - (self.start_time or datetime.now())).total_seconds() / 60
            },
            'performance_summary': {
                'avg_cpu_percent': round(avg_cpu, 2),
                'avg_memory_percent': round(avg_memory, 2),
                'max_cpu_percent': round(max_cpu, 2),
                'max_memory_percent': round(max_memory, 2),
                'total_alerts': len(self.alerts)
            },
            'alerts': self.alerts,
            'recommendations': self._generate_recommendations(avg_cpu, avg_memory, max_cpu, max_memory)
        }
        
        # Save report
        report_file = f"system_monitoring_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📋 Monitoring report saved: {report_file}")
        self._print_summary(report)
    
    def _generate_recommendations(self, avg_cpu: float, avg_memory: float, max_cpu: float, max_memory: float) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        if avg_cpu > 70:
            recommendations.append("Consider CPU optimization or scaling")
        if avg_memory > 70:
            recommendations.append("Consider memory optimization or additional RAM")
        if max_cpu > 95:
            recommendations.append("Investigate CPU spikes - possible inefficient loops")
        if max_memory > 95:
            recommendations.append("Memory usage critical - check for memory leaks")
        
        if not recommendations:
            recommendations.append("System performance is optimal")
        
        return recommendations
    
    def _print_summary(self, report: Dict[str, Any]):
        """Print monitoring summary"""
        print("\n" + "="*60)
        print("🔍 SYSTEM MONITORING SUMMARY")
        print("="*60)
        print(f"Duration: {report['monitoring_period']['duration_minutes']:.1f} minutes")
        print(f"Average CPU: {report['performance_summary']['avg_cpu_percent']}%")
        print(f"Average Memory: {report['performance_summary']['avg_memory_percent']}%")
        print(f"Peak CPU: {report['performance_summary']['max_cpu_percent']}%")
        print(f"Peak Memory: {report['performance_summary']['max_memory_percent']}%")
        print(f"Total Alerts: {report['performance_summary']['total_alerts']}")
        print("\n💡 RECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"   • {rec}")
        print("="*60)

class FSATAutomationSuite:
    """Automation tools for FSOT AI system"""
    
    def __init__(self):
        self.monitor = FSATSystemMonitor()
    
    def run_health_check(self) -> Dict[str, Any]:
        """Comprehensive system health check"""
        logger.info("🏥 Running comprehensive health check...")
        
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'python_environment': self._check_python_environment(),
            'dependencies': self._check_dependencies(),
            'system_resources': self._check_system_resources(),
            'fsot_components': self._check_fsot_components(),
            'overall_health': 'UNKNOWN'
        }
        
        # Determine overall health
        issues = sum(1 for check in health_status.values() if isinstance(check, dict) and check.get('status') == 'ERROR')
        if issues == 0:
            health_status['overall_health'] = 'EXCELLENT'
        elif issues <= 2:
            health_status['overall_health'] = 'GOOD'
        else:
            health_status['overall_health'] = 'NEEDS_ATTENTION'
        
        self._print_health_report(health_status)
        return health_status
    
    def _check_python_environment(self) -> Dict[str, Any]:
        """Check Python environment"""
        try:
            import sys
            return {
                'status': 'OK',
                'version': sys.version,
                'executable': sys.executable,
                'path_count': len(sys.path)
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}
    
    def _check_dependencies(self) -> Dict[str, Any]:
        """Check critical dependencies"""
        critical_libs = ['numpy', 'torch', 'transformers', 'matplotlib', 'gradio']
        results = {}
        
        for lib in critical_libs:
            try:
                __import__(lib)
                results[lib] = 'OK'
            except ImportError:
                results[lib] = 'MISSING'
        
        missing = [lib for lib, status in results.items() if status == 'MISSING']
        return {
            'status': 'ERROR' if missing else 'OK',
            'libraries': results,
            'missing_libraries': missing
        }
    
    def _check_system_resources(self) -> Dict[str, Any]:
        """Check system resources"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'status': 'OK',
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent,
                'available_memory_gb': round(memory.available / (1024**3), 2)
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}
    
    def _check_fsot_components(self) -> Dict[str, Any]:
        """Check FSOT-specific components"""
        try:
            # Test FSOT imports
            sys.path.insert(0, _os.fspath(_REPO_ROOT / 'FSOT_Clean_System'))
            from fsot_2_0_foundation import FSOTCore, FSOTDomain
            
            # Test brain system
            sys.path.insert(0, _os.fspath(_REPO_ROOT))
            from brain_system import NeuromorphicBrainSystem
            
            return {
                'status': 'OK',
                'fsot_core': 'Available',
                'brain_system': 'Available',
                'components_tested': 2
            }
        except Exception as e:
            return {'status': 'ERROR', 'error': str(e)}
    
    def _print_health_report(self, health_status: Dict[str, Any]):
        """Print health check report"""
        print("\n" + "="*60)
        print("🏥 SYSTEM HEALTH CHECK REPORT")
        print("="*60)
        print(f"Overall Health: {health_status['overall_health']}")
        print(f"Timestamp: {health_status['timestamp']}")
        print()
        
        for component, details in health_status.items():
            if component in ['timestamp', 'overall_health']:
                continue
                
            if isinstance(details, dict):
                status = details.get('status', 'UNKNOWN')
                emoji = "✅" if status == 'OK' else "❌"
                print(f"{emoji} {component.replace('_', ' ').title()}: {status}")
                
                if status == 'ERROR' and 'error' in details:
                    print(f"   Error: {details['error']}")
        print("="*60)
    
    def run_performance_test(self, duration_minutes: int = 2):
        """Run performance monitoring test"""
        logger.info(f"🚀 Starting {duration_minutes}-minute performance test...")
        
        # Start monitoring
        monitor_thread = self.monitor.start_monitoring(duration_minutes)
        
        # Run some test operations
        self._run_test_operations()
        
        # Wait for monitoring to complete
        monitor_thread.join()
        
        logger.info("✅ Performance test completed")
    
    def _run_test_operations(self):
        """Run test operations to generate load"""
        logger.info("🧪 Running test operations...")
        
        # CPU test
        for i in range(10):
            sum(x**2 for x in range(10000))
            time.sleep(0.1)
        
        # Memory test
        test_data = [list(range(1000)) for _ in range(100)]
        del test_data
        
        logger.info("✅ Test operations completed")

def main():
    """Main automation suite"""
    print("🤖 FSOT SYSTEM AUTOMATION SUITE")
    print("="*50)
    
    suite = FSATAutomationSuite()
    
    # Run health check
    health_status = suite.run_health_check()
    
    # Run performance test if system is healthy
    if health_status['overall_health'] in ['EXCELLENT', 'GOOD']:
        print("\n🚀 System healthy - running performance test...")
        suite.run_performance_test(duration_minutes=1)
    else:
        print("\n⚠️ System needs attention - skipping performance test")
    
    print("\n✅ Automation suite completed!")

if __name__ == "__main__":
    main()
