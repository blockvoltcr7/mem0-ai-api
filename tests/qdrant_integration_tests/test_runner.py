"""
Qdrant Integration Test Runner

Provides utilities for running the Qdrant integration tests with different
configurations, generating reports, and managing test execution.

Author: AI Tutor Development Team
Version: 1.0
"""

import subprocess
import sys
import os
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

class QdrantTestRunner:
    """Test runner for Qdrant integration tests."""
    
    def __init__(self, project_root: str = None):
        """Initialize the test runner."""
        if project_root:
            self.project_root = Path(project_root)
        else:
            # If we're in the test directory, go up to project root
            current_path = Path.cwd()
            if current_path.name == "qdrant_integration_tests":
                self.project_root = current_path.parent.parent
            else:
                self.project_root = current_path
        
        self.test_dir = self.project_root / "tests" / "qdrant_integration_tests"
        self.allure_results_dir = self.project_root / "allure-results"
        self.allure_reports_dir = self.project_root / "allure-reports"
        
    def run_tests(
        self,
        test_categories: List[str] = None,
        markers: List[str] = None,
        verbose: bool = True,
        generate_report: bool = True,
        open_report: bool = False,
        parallel: bool = False,
        max_workers: int = 4
    ) -> Dict[str, Any]:
        """
        Run Qdrant integration tests with specified configuration.
        
        Args:
            test_categories: List of test categories to run (health, chat, memory, etc.)
            markers: List of pytest markers to filter tests
            verbose: Enable verbose output
            generate_report: Generate Allure report after tests
            open_report: Open Allure report in browser
            parallel: Run tests in parallel
            max_workers: Maximum number of parallel workers
            
        Returns:
            Dictionary with test execution results
        """
        print("🚀 Starting Qdrant Integration Tests")
        print(f"📁 Test Directory: {self.test_dir}")
        print(f"📊 Results Directory: {self.allure_results_dir}")
        
        # Prepare pytest command
        cmd = self._build_pytest_command(
            test_categories=test_categories,
            markers=markers,
            verbose=verbose,
            parallel=parallel,
            max_workers=max_workers
        )
        
        print(f"🔧 Command: {' '.join(cmd)}")
        print("=" * 80)
        
        # Execute tests
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=False, text=True)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Prepare results
        test_results = {
            "exit_code": result.returncode,
            "execution_time_seconds": execution_time,
            "success": result.returncode == 0,
            "command": " ".join(cmd)
        }
        
        print("=" * 80)
        print(f"✅ Tests completed in {execution_time:.2f} seconds")
        print(f"📋 Exit code: {result.returncode}")
        
        # Generate and open report if requested
        if generate_report and self.allure_results_dir.exists():
            self._generate_allure_report(open_report=open_report)
        
        return test_results
    
    def _build_pytest_command(
        self,
        test_categories: List[str] = None,
        markers: List[str] = None,
        verbose: bool = True,
        parallel: bool = False,
        max_workers: int = 4
    ) -> List[str]:
        """Build the pytest command with specified options."""
        cmd = ["pytest"]
        
        # Add test directory
        if test_categories:
            # Run specific test files based on categories
            for category in test_categories:
                test_file = self.test_dir / f"test_{category}_endpoints.py"
                if category == "memory":
                    test_file = self.test_dir / "test_memory_scenarios.py"
                elif category == "performance":
                    test_file = self.test_dir / "test_performance_benchmarks.py"
                
                if test_file.exists():
                    cmd.append(str(test_file))
        else:
            # Run all tests in the directory
            cmd.append(str(self.test_dir))
        
        # Add markers
        if markers:
            for marker in markers:
                cmd.extend(["-m", marker])
        
        # Add Allure reporting
        cmd.extend(["--alluredir", str(self.allure_results_dir)])
        
        # Add verbosity
        if verbose:
            cmd.append("-v")
        
        # Add parallel execution
        if parallel:
            cmd.extend(["-n", str(max_workers)])
        
        # Add additional options
        cmd.extend([
            "--tb=short",  # Short traceback format
            "--strict-markers",  # Strict marker checking
            "--disable-warnings"  # Disable warnings for cleaner output
        ])
        
        return cmd
    
    def _generate_allure_report(self, open_report: bool = False) -> None:
        """Generate Allure report from test results."""
        print("📊 Generating Allure report...")
        
        # Ensure reports directory exists
        self.allure_reports_dir.mkdir(exist_ok=True)
        
        # Generate report
        generate_cmd = [
            "allure", "generate", 
            str(self.allure_results_dir),
            "-o", str(self.allure_reports_dir),
            "--clean"
        ]
        
        try:
            subprocess.run(generate_cmd, check=True, capture_output=True)
            print(f"✅ Report generated: {self.allure_reports_dir}")
            
            if open_report:
                self._open_allure_report()
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to generate Allure report: {e}")
        except FileNotFoundError:
            print("❌ Allure not found. Install with: pip install allure-pytest")
    
    def _open_allure_report(self) -> None:
        """Open Allure report in browser."""
        print("🌐 Opening Allure report in browser...")
        
        serve_cmd = ["allure", "serve", str(self.allure_results_dir)]
        
        try:
            subprocess.Popen(serve_cmd)
            print("✅ Allure report opened in browser")
        except FileNotFoundError:
            print("❌ Allure not found. Install with: pip install allure-pytest")
    
    def list_available_tests(self) -> Dict[str, List[str]]:
        """List all available tests organized by category."""
        tests = {
            "health": [],
            "chat": [],
            "memory": [],
            "performance": []
        }
        
        # Scan test files
        for test_file in self.test_dir.glob("test_*.py"):
            if test_file.name == "test_runner.py":
                continue
                
            # Read file to extract test methods
            try:
                with open(test_file, 'r') as f:
                    content = f.read()
                    
                # Extract test method names
                import re
                test_methods = re.findall(r'def (test_\w+)', content)
                
                # Categorize based on file name
                if "health" in test_file.name:
                    tests["health"].extend(test_methods)
                elif "chat" in test_file.name:
                    tests["chat"].extend(test_methods)
                elif "memory" in test_file.name:
                    tests["memory"].extend(test_methods)
                elif "performance" in test_file.name:
                    tests["performance"].extend(test_methods)
                    
            except Exception as e:
                print(f"Warning: Could not read {test_file}: {e}")
        
        return tests
    
    def run_smoke_tests(self) -> Dict[str, Any]:
        """Run a quick smoke test suite."""
        print("💨 Running smoke tests...")
        
        return self.run_tests(
            markers=["health", "integration"],
            verbose=True,
            generate_report=False,
            parallel=False
        )
    
    def run_full_suite(self) -> Dict[str, Any]:
        """Run the complete test suite."""
        print("🎯 Running full test suite...")
        
        return self.run_tests(
            verbose=True,
            generate_report=True,
            open_report=True,
            parallel=True,
            max_workers=4
        )
    
    def run_performance_tests(self) -> Dict[str, Any]:
        """Run only performance tests."""
        print("⚡ Running performance tests...")
        
        return self.run_tests(
            test_categories=["performance"],
            markers=["performance"],
            verbose=True,
            generate_report=True,
            parallel=False  # Performance tests should run sequentially
        )
    
    def clean_results(self) -> None:
        """Clean previous test results and reports."""
        print("🧹 Cleaning previous test results...")
        
        import shutil
        
        if self.allure_results_dir.exists():
            shutil.rmtree(self.allure_results_dir)
            print(f"✅ Cleaned: {self.allure_results_dir}")
        
        if self.allure_reports_dir.exists():
            shutil.rmtree(self.allure_reports_dir)
            print(f"✅ Cleaned: {self.allure_reports_dir}")


def main():
    """Main CLI interface for the test runner."""
    parser = argparse.ArgumentParser(
        description="Qdrant Integration Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_runner.py --smoke                    # Run smoke tests
  python test_runner.py --full                     # Run full suite
  python test_runner.py --performance              # Run performance tests
  python test_runner.py --categories health chat   # Run specific categories
  python test_runner.py --markers integration      # Run tests with specific markers
  python test_runner.py --list                     # List available tests
  python test_runner.py --clean                    # Clean previous results
        """
    )
    
    # Test execution options
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--full", action="store_true", help="Run full test suite")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    
    # Filtering options
    parser.add_argument("--categories", nargs="+", 
                       choices=["health", "chat", "memory", "performance"],
                       help="Test categories to run")
    parser.add_argument("--markers", nargs="+", 
                       help="Pytest markers to filter tests")
    
    # Execution options
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers")
    parser.add_argument("--no-report", action="store_true", help="Skip Allure report generation")
    parser.add_argument("--open-report", action="store_true", help="Open report in browser")
    
    # Utility options
    parser.add_argument("--list", action="store_true", help="List available tests")
    parser.add_argument("--clean", action="store_true", help="Clean previous results")
    parser.add_argument("--project-root", help="Project root directory")
    
    args = parser.parse_args()
    
    # Initialize test runner
    runner = QdrantTestRunner(project_root=args.project_root)
    
    # Handle utility commands
    if args.clean:
        runner.clean_results()
        return
    
    if args.list:
        tests = runner.list_available_tests()
        print("📋 Available Tests:")
        for category, test_list in tests.items():
            print(f"\n{category.upper()}:")
            for test in test_list:
                print(f"  • {test}")
        return
    
    # Execute tests based on arguments
    if args.smoke:
        result = runner.run_smoke_tests()
    elif args.full:
        result = runner.run_full_suite()
    elif args.performance:
        result = runner.run_performance_tests()
    else:
        # Custom test execution
        result = runner.run_tests(
            test_categories=args.categories,
            markers=args.markers,
            verbose=True,
            generate_report=not args.no_report,
            open_report=args.open_report,
            parallel=args.parallel,
            max_workers=args.workers
        )
    
    # Print final results
    print("\n" + "=" * 80)
    print("📊 TEST EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Success: {'✅' if result['success'] else '❌'}")
    print(f"Exit Code: {result['exit_code']}")
    print(f"Execution Time: {result['execution_time_seconds']:.2f} seconds")
    print(f"Command: {result['command']}")
    
    # Exit with appropriate code
    sys.exit(result['exit_code'])


if __name__ == "__main__":
    main() 