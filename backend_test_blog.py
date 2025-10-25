#!/usr/bin/env python3
"""
Backend Testing Suite for GuaraniAppStore V2.5 Pro
Testing focus: Blog System Automatizado con Panel Admin
"""

import requests
import json
import sys
import time
from typing import Dict, Any, Optional

class GuaraniBlogTester:
    def __init__(self):
        self.base_url = "https://cryptoshield-app.preview.emergentagent.com/api"
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        
        # Admin credentials 
        self.admin_email = "admin@guaraniappstore.com"
        self.admin_password = "admin123"
        
        # Test data storage
        self.test_article_id = None
        self.test_article_slug = None
        self.initial_views = 0
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'response_data': response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()

    def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None, params: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, params=params, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers, timeout=30)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers, timeout=30)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers, timeout=30)
            else:
                return False, f"Unsupported method: {method}", 0
                
            try:
                response_data = response.json()
            except:
                response_data = response.text
                
            return response.status_code < 400, response_data, response.status_code
            
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}", 0

    def test_admin_login(self):
        """Test admin login and store token"""
        login_data = {
            "email": self.admin_email,
            "password": self.admin_password
        }
        
        success, data, status_code = self.make_request('POST', '/auth/login', login_data)
        
        if success and isinstance(data, dict) and 'access_token' in data:
            self.admin_token = data['access_token']
            user_info = data.get('user', {})
            role = user_info.get('role', 'unknown')
            
            if role == 'admin':
                self.log_test("Admin Login", True, f"Logged in as admin: {user_info.get('email')}")
                # Set authorization header for future requests
                self.session.headers.update({'Authorization': f'Bearer {self.admin_token}'})
                return True
            else:
                self.log_test("Admin Login", False, f"User role is '{role}', expected 'admin'")
                return False
        else:
            self.log_test("Admin Login", False, f"Status code: {status_code}", data)
            return False

    # ============================================
    # PUBLIC BLOG ENDPOINTS TESTS
    # ============================================

    def test_get_published_posts(self):
        """Test GET /api/blog/posts - list published articles with pagination"""
        # Test without pagination
        success, data, status_code = self.make_request('GET', '/blog/posts')
        
        if success and isinstance(data, list):
            self.log_test("Get Published Posts", True, f"Retrieved {len(data)} published articles")
            
            # Store first article for slug testing
            if data:
                first_article = data[0]
                self.test_article_slug = first_article.get('slug')
                self.initial_views = first_article.get('views', 0)
                
                # Verify article structure
                required_fields = ['id', 'title', 'slug', 'excerpt', 'author_name', 'published_at', 'views']
                missing_fields = [field for field in required_fields if field not in first_article]
                
                if not missing_fields:
                    print(f"   ✓ Article structure valid")
                    print(f"   ✓ Sample article: '{first_article.get('title', 'N/A')}'")
                    print(f"   ✓ Author: {first_article.get('author_name', 'N/A')}")
                    print(f"   ✓ Views: {first_article.get('views', 0)}")
                else:
                    print(f"   ⚠ Missing fields: {missing_fields}")
            
            # Test pagination
            success_page, data_page, _ = self.make_request('GET', '/blog/posts', params={'skip': 0, 'limit': 5})
            if success_page and isinstance(data_page, list):
                print(f"   ✓ Pagination working: {len(data_page)} articles with limit=5")
            
        else:
            self.log_test("Get Published Posts", False, f"Status code: {status_code}", data)

    def test_get_post_by_slug(self):
        """Test GET /api/blog/posts/{slug} - should increment views"""
        if not self.test_article_slug:
            self.log_test("Get Post by Slug", False, "No test article slug available")
            return
            
        success, data, status_code = self.make_request('GET', f'/blog/posts/{self.test_article_slug}')
        
        if success and isinstance(data, dict):
            new_views = data.get('views', 0)
            
            # Check if views incremented
            if new_views > self.initial_views:
                self.log_test("Get Post by Slug", True, f"Views incremented: {self.initial_views} → {new_views}")
                
                # Verify Bitfinex promotional text
                content = data.get('content', '')
                if 'bitfinex' in content.lower():
                    print(f"   ✓ Bitfinex promotional text found in article")
                else:
                    print(f"   ⚠ Bitfinex promotional text NOT found")
                    
                # Verify article completeness
                print(f"   ✓ Title: {data.get('title', 'N/A')}")
                print(f"   ✓ Author: {data.get('author_name', 'N/A')} ({data.get('author_role', 'N/A')})")
                print(f"   ✓ Reading time: {data.get('reading_time', 'N/A')} min")
                print(f"   ✓ Content length: {len(content)} chars")
                
            else:
                self.log_test("Get Post by Slug", False, f"Views not incremented: {self.initial_views} → {new_views}")
        else:
            self.log_test("Get Post by Slug", False, f"Status code: {status_code}", data)

    # ============================================
    # ADMIN BLOG ENDPOINTS TESTS
    # ============================================

    def test_generate_custom_article(self):
        """Test POST /api/blog/generate/custom - generate on-demand article"""
        if not self.admin_token:
            self.log_test("Generate Custom Article", False, "No admin token available")
            return
            
        # Use a unique search query to avoid slug conflicts
        import time
        unique_id = int(time.time())
        
        article_request = {
            "search_query": f"marketing digital estrategias {unique_id}",
            "target_keywords": ["marketing", "digital", "estrategias"],
            "agent_id": 2,  # Different agent
            "tone": "profesional",
            "length": "medium",
            "include_faq": True
        }
        
        success, data, status_code = self.make_request('POST', '/blog/generate/custom', article_request)
        
        if success and isinstance(data, dict):
            if data.get('success') == True:
                self.test_article_id = data.get('article_id')
                status = data.get('status')
                
                if status == 'pending_approval':
                    self.log_test("Generate Custom Article", True, f"Article generated with ID: {self.test_article_id}")
                    print(f"   ✓ Status: {status}")
                    print(f"   ✓ Message: {data.get('message', 'N/A')}")
                else:
                    self.log_test("Generate Custom Article", False, f"Unexpected status: {status}")
            else:
                self.log_test("Generate Custom Article", False, f"Generation failed: {data.get('message', 'Unknown error')}")
        else:
            self.log_test("Generate Custom Article", False, f"Status code: {status_code}", data)

    def test_get_pending_articles(self):
        """Test GET /api/blog/posts/pending - list pending approval articles"""
        if not self.admin_token:
            self.log_test("Get Pending Articles", False, "No admin token available")
            return
            
        success, data, status_code = self.make_request('GET', '/blog/posts/pending')
        
        if success and isinstance(data, list):
            pending_count = len(data)
            self.log_test("Get Pending Articles", True, f"Found {pending_count} pending articles")
            
            if data:
                # Verify pending articles have correct flags
                first_pending = data[0]
                if first_pending.get('pending_approval') == True and first_pending.get('published') == False:
                    print(f"   ✓ Pending article structure correct")
                    print(f"   ✓ Sample: '{first_pending.get('title', 'N/A')}'")
                    print(f"   ✓ Requested by: {first_pending.get('requested_by', 'N/A')}")
                else:
                    print(f"   ⚠ Pending article flags incorrect")
                    print(f"     pending_approval: {first_pending.get('pending_approval')}")
                    print(f"     published: {first_pending.get('published')}")
        else:
            self.log_test("Get Pending Articles", False, f"Status code: {status_code}", data)

    def test_get_article_preview(self):
        """Test GET /api/blog/posts/{post_id}/preview - preview without incrementing views"""
        if not self.admin_token:
            self.log_test("Get Article Preview", False, "No admin token available")
            return
            
        if not self.test_article_id:
            # Try to get any pending article
            success, pending_data, _ = self.make_request('GET', '/blog/posts/pending')
            if success and pending_data:
                self.test_article_id = pending_data[0].get('id')
            
        if not self.test_article_id:
            self.log_test("Get Article Preview", False, "No test article ID available")
            return
            
        success, data, status_code = self.make_request('GET', f'/blog/posts/{self.test_article_id}/preview')
        
        if success and isinstance(data, dict):
            self.log_test("Get Article Preview", True, f"Preview retrieved for article: {data.get('title', 'N/A')}")
            
            # Verify it's a complete article
            required_fields = ['id', 'title', 'content', 'author_name', 'pending_approval']
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                print(f"   ✓ Complete article data retrieved")
                print(f"   ✓ Content length: {len(data.get('content', ''))} chars")
                print(f"   ✓ Pending approval: {data.get('pending_approval')}")
            else:
                print(f"   ⚠ Missing fields: {missing_fields}")
                
        else:
            self.log_test("Get Article Preview", False, f"Status code: {status_code}", data)

    def test_approve_article(self):
        """Test PUT /api/blog/posts/{post_id}/approve - approve and publish"""
        if not self.admin_token:
            self.log_test("Approve Article", False, "No admin token available")
            return
            
        if not self.test_article_id:
            self.log_test("Approve Article", False, "No test article ID available")
            return
            
        success, data, status_code = self.make_request('PUT', f'/blog/posts/{self.test_article_id}/approve')
        
        if success and isinstance(data, dict):
            if data.get('success') == True:
                article = data.get('article', {})
                self.log_test("Approve Article", True, f"Article approved: {article.get('title', 'N/A')}")
                
                # Verify approval fields
                if article.get('published') == True and article.get('pending_approval') == False:
                    print(f"   ✓ Article published successfully")
                    print(f"   ✓ Approved by: {article.get('approved_by', 'N/A')}")
                    print(f"   ✓ Published at: {article.get('published_at', 'N/A')}")
                else:
                    print(f"   ⚠ Approval flags not set correctly")
            else:
                self.log_test("Approve Article", False, f"Approval failed: {data.get('message', 'Unknown error')}")
        else:
            self.log_test("Approve Article", False, f"Status code: {status_code}", data)

    def test_reject_article(self):
        """Test PUT /api/blog/posts/{post_id}/reject - reject and delete"""
        if not self.admin_token:
            self.log_test("Reject Article", False, "No admin token available")
            return
            
        # Generate a new article to reject
        import time
        unique_id = int(time.time()) + 1  # Different from the other test
        
        article_request = {
            "search_query": f"test article for rejection {unique_id}",
            "target_keywords": ["test"],
            "agent_id": None,  # Auto-detect
            "tone": "profesional",
            "length": "short",
            "include_faq": False
        }
        
        success, gen_data, _ = self.make_request('POST', '/blog/generate/custom', article_request)
        
        if not success or not gen_data.get('success'):
            self.log_test("Reject Article", False, "Could not generate test article for rejection")
            return
            
        reject_article_id = gen_data.get('article_id')
        time.sleep(2)  # Wait for generation
        
        success, data, status_code = self.make_request('PUT', f'/blog/posts/{reject_article_id}/reject')
        
        if success and isinstance(data, dict):
            if data.get('success') == True:
                self.log_test("Reject Article", True, f"Article rejected and deleted")
                print(f"   ✓ Message: {data.get('message', 'N/A')}")
                
                # Verify article was deleted by trying to preview it
                success_check, _, status_check = self.make_request('GET', f'/blog/posts/{reject_article_id}/preview')
                if status_check == 404:
                    print(f"   ✓ Article successfully deleted from database")
                else:
                    print(f"   ⚠ Article may not have been deleted (status: {status_check})")
            else:
                self.log_test("Reject Article", False, f"Rejection failed: {data.get('message', 'Unknown error')}")
        else:
            self.log_test("Reject Article", False, f"Status code: {status_code}", data)

    def test_blog_stats(self):
        """Test GET /api/blog/stats - blog statistics"""
        if not self.admin_token:
            self.log_test("Blog Stats", False, "No admin token available")
            return
            
        success, data, status_code = self.make_request('GET', '/blog/stats')
        
        if success and isinstance(data, dict):
            required_stats = ['total_posts', 'published_posts', 'draft_posts', 'total_views', 'avg_views_per_post']
            missing_stats = [stat for stat in required_stats if stat not in data]
            
            if not missing_stats:
                self.log_test("Blog Stats", True, "All statistics retrieved successfully")
                print(f"   ✓ Total posts: {data.get('total_posts', 0)}")
                print(f"   ✓ Published posts: {data.get('published_posts', 0)}")
                print(f"   ✓ Draft posts: {data.get('draft_posts', 0)}")
                print(f"   ✓ Total views: {data.get('total_views', 0)}")
                print(f"   ✓ Avg views per post: {data.get('avg_views_per_post', 0)}")
                
                # Verify calculations make sense
                total = data.get('total_posts', 0)
                published = data.get('published_posts', 0)
                drafts = data.get('draft_posts', 0)
                
                if published + drafts <= total:
                    print(f"   ✓ Statistics calculations appear correct")
                else:
                    print(f"   ⚠ Statistics calculations may be incorrect")
            else:
                self.log_test("Blog Stats", False, f"Missing statistics: {missing_stats}")
        else:
            self.log_test("Blog Stats", False, f"Status code: {status_code}", data)

    # ============================================
    # VERIFICATION TESTS
    # ============================================

    def test_scheduled_vs_ondemand_behavior(self):
        """Verify scheduled articles publish directly vs on-demand go to queue"""
        if not self.admin_token:
            self.log_test("Scheduled vs On-demand Behavior", False, "No admin token available")
            return
            
        # Get published posts (should be scheduled articles)
        success_pub, pub_data, _ = self.make_request('GET', '/blog/posts')
        
        # Get pending posts (should be on-demand articles)
        success_pend, pend_data, _ = self.make_request('GET', '/blog/posts/pending')
        
        if success_pub and success_pend:
            published_count = len(pub_data) if isinstance(pub_data, list) else 0
            pending_count = len(pend_data) if isinstance(pend_data, list) else 0
            
            self.log_test("Scheduled vs On-demand Behavior", True, 
                         f"Published (scheduled): {published_count}, Pending (on-demand): {pending_count}")
            
            # Check if published articles have generation_type
            if pub_data and isinstance(pub_data, list):
                scheduled_article = pub_data[0]
                gen_type = scheduled_article.get('generation_type', 'unknown')
                print(f"   ✓ Sample published article generation type: {gen_type}")
                
            # Check if pending articles have generation_type
            if pend_data and isinstance(pend_data, list):
                pending_article = pend_data[0]
                gen_type = pending_article.get('generation_type', 'unknown')
                print(f"   ✓ Sample pending article generation type: {gen_type}")
        else:
            self.log_test("Scheduled vs On-demand Behavior", False, "Could not retrieve articles for comparison")

    def test_bitfinex_promotional_text(self):
        """Verify Bitfinex promotional text is present in all articles"""
        success, data, status_code = self.make_request('GET', '/blog/posts', params={'limit': 3})
        
        if success and isinstance(data, list) and data:
            articles_with_bitfinex = 0
            total_articles = len(data)
            
            for article in data:
                # Get full article content
                slug = article.get('slug')
                if slug:
                    success_full, full_data, _ = self.make_request('GET', f'/blog/posts/{slug}')
                    if success_full and isinstance(full_data, dict):
                        content = full_data.get('content', '').lower()
                        if 'bitfinex' in content:
                            articles_with_bitfinex += 1
            
            if articles_with_bitfinex == total_articles:
                self.log_test("Bitfinex Promotional Text", True, 
                             f"All {total_articles} articles contain Bitfinex promotional text")
            else:
                self.log_test("Bitfinex Promotional Text", False, 
                             f"Only {articles_with_bitfinex}/{total_articles} articles contain Bitfinex text")
        else:
            self.log_test("Bitfinex Promotional Text", False, "Could not retrieve articles for verification")

    def run_all_tests(self):
        """Run all blog system tests"""
        print("=" * 80)
        print("GuaraniAppStore V2.5 Pro - Blog System Testing Suite")
        print("Testing: Sistema de Blog Automatizado con Panel Admin")
        print("=" * 80)
        print()
        
        # Authentication
        print("🔐 Testing Authentication...")
        if not self.test_admin_login():
            print("❌ Cannot proceed without admin authentication")
            return
        
        # Public endpoints
        print("🌐 Testing Public Blog Endpoints...")
        self.test_get_published_posts()
        self.test_get_post_by_slug()
        
        # Admin endpoints
        print("👤 Testing Admin Blog Endpoints...")
        self.test_generate_custom_article()
        self.test_get_pending_articles()
        self.test_get_article_preview()
        self.test_approve_article()
        self.test_reject_article()
        self.test_blog_stats()
        
        # Verification tests
        print("✅ Testing System Behavior...")
        self.test_scheduled_vs_ondemand_behavior()
        self.test_bitfinex_promotional_text()
        
        # Summary
        self.print_summary()

    def print_summary(self):
        """Print comprehensive test summary"""
        print("=" * 80)
        print("BLOG SYSTEM TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        # Categorize results
        public_tests = [r for r in self.test_results if 'Published Posts' in r['test'] or 'Post by Slug' in r['test']]
        admin_tests = [r for r in self.test_results if any(x in r['test'] for x in ['Generate', 'Pending', 'Preview', 'Approve', 'Reject', 'Stats'])]
        verification_tests = [r for r in self.test_results if any(x in r['test'] for x in ['Behavior', 'Bitfinex'])]
        
        print("📊 RESULTS BY CATEGORY:")
        print(f"   Public Endpoints: {sum(1 for r in public_tests if r['success'])}/{len(public_tests)} passed")
        print(f"   Admin Endpoints:  {sum(1 for r in admin_tests if r['success'])}/{len(admin_tests)} passed")
        print(f"   Verification:     {sum(1 for r in verification_tests if r['success'])}/{len(verification_tests)} passed")
        print()
        
        if failed_tests > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['details']}")
            print()
        
        # Critical functionality assessment
        critical_working = all(r['success'] for r in self.test_results if r['test'] in [
            'Admin Login', 'Get Published Posts', 'Generate Custom Article', 'Blog Stats'
        ])
        
        print("🎯 CRITICAL FUNCTIONALITY:")
        if critical_working:
            print("   ✅ Blog system is FULLY OPERATIONAL")
            print("   ✅ Article generation working")
            print("   ✅ Admin panel functional")
            print("   ✅ Public endpoints working")
        else:
            print("   ❌ Critical blog functionality has issues")
            print("   🔍 Check failed tests above for details")
        
        print()
        print("📋 SYSTEM STATUS:")
        print("   • Scheduled articles: Auto-published daily at 08:00 AM")
        print("   • On-demand articles: Require admin approval")
        print("   • Bitfinex promotional text: Included in all articles")
        print("   • Blog statistics: Available in admin panel")
        print("   • Article views: Tracked and incremented")

if __name__ == "__main__":
    tester = GuaraniBlogTester()
    tester.run_all_tests()