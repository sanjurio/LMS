import os
from datetime import datetime, timedelta
from main import app
from app.models import db, User, Interest, Course, Lesson, UserInterest, CourseInterest, UserLessonProgress, ForumTopic, ForumReply, UserActivity, MandatoryCourse, Assignment, Question

def populate():
    with app.app_context():
        # Clear existing data (optional, but good for clean slate)
        # Note: Be careful with relationships
        print("Populating dummy data...")
        
        # 1. Teams (Interests)
        teams = [
            ("Engineering", "Core engineering team focusing on product development."),
            ("Marketing", "Promoting products and managing brand identity."),
            ("Sales", "Driving revenue and customer acquisition."),
            ("HR", "Human resources and talent management."),
            ("Operations", "Daily business operations and logistics."),
            ("Customer Support", "Assisting customers with technical issues.")
        ]
        
        team_objs = []
        for name, desc in teams:
            team = Interest.query.filter_by(name=name).first()
            if not team:
                team = Interest(name=name, description=desc)
                db.session.add(team)
            team_objs.append(team)
        db.session.commit()
        
        # 2. Users
        admin = User.query.filter_by(email="admin@example.com").first()
        if not admin:
            admin = User(username="admin", email="admin@example.com", is_admin=True, is_approved=True)
            admin.set_password("Admin123")
            db.session.add(admin)
        
        users_data = [
            ("john_doe", "john@thbs.com", "User123!", "thbs.com", 1, True),
            ("jane_smith", "jane@bt.com", "User123!", "bt.com", 2, True),
            ("bob_jones", "bob@thbs.com", "User123!", "thbs.com", 3, True),
            ("alice_williams", "alice@bt.com", "User123!", "bt.com", 4, True),
            ("pending_user", "pending@thbs.com", "User123!", "thbs.com", 1, False),
            ("sarah_connor", "sarah@thbs.com", "User123!", "thbs.com", 1, False),
            ("mike_ross", "mike@bt.com", "User123!", "bt.com", 1, False),
            ("rachel_zane", "rachel@thbs.com", "User123!", "thbs.com", 1, False),
            ("harvey_specter", "harvey@bt.com", "User123!", "bt.com", 1, False)
        ]
        
        user_objs = []
        for uname, email, pwd, domain, level, approved in users_data:
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(username=uname, email=email, is_approved=approved, access_level=level, email_domain=domain)
                user.set_password(pwd)
                db.session.add(user)
            user_objs.append(user)
        db.session.commit()
        
        # 3. User Interests
        for user in user_objs:
            if user.is_approved:
                # Assign 2 random teams to each user
                for i in range(2):
                    team = team_objs[(user.id + i) % len(team_objs)]
                    ui = UserInterest.query.filter_by(user_id=user.id, interest_id=team.id).first()
                    if not ui:
                        ui = UserInterest(user_id=user.id, interest_id=team.id, access_granted=True, granted_at=datetime.utcnow(), granted_by=admin.id)
                        db.session.add(ui)
        db.session.commit()
        
        # 4. Courses
        courses_data = [
            ("Introduction to Erlang", "Learn the basics of Erlang programming language.", 1, "Engineering"),
            ("Advanced OTP Patterns", "Master advanced OTP behaviors and design patterns.", 2, "Engineering"),
            ("Erlang for Enterprise-thbs", "Restricted course for THBS employees.", 3, "Engineering"),
            ("Marketing Basics", "Foundations of modern marketing.", 1, "Marketing"),
            ("Sales Strategy 2024", "Advanced sales techniques for the current year.", 2, "Sales"),
            ("Employee Relations", "Best practices for HR professionals.", 1, "HR")
        ]
        
        course_objs = []
        for title, desc, level, team_name in courses_data:
            course = Course.query.filter_by(title=title).first()
            if not course:
                course = Course(title=title, description=desc, required_level=level, created_by=admin.id)
                db.session.add(course)
                db.session.flush() # Get ID
                
                # Link to team
                team = Interest.query.filter_by(name=team_name).first()
                if team:
                    ci = CourseInterest(course_id=course.id, interest_id=team.id)
                    db.session.add(ci)
            course_objs.append(course)
        db.session.commit()
        
        # 5. Lessons
        for course in course_objs:
            for i in range(1, 4):
                lesson = Lesson.query.filter_by(course_id=course.id, order=i).first()
                if not lesson:
                    lesson = Lesson(
                        title=f"Lesson {i} of {course.title}",
                        content=f"This is the detailed content for lesson {i} in the course '{course.title}'. It covers various aspects of the topic.",
                        content_type='mixed' if i == 2 else 'text',
                        video_url="https://www.youtube.com/embed/dQw4w9WgXcQ" if i == 2 else None,
                        course_id=course.id,
                        order=i
                    )
                    db.session.add(lesson)
        db.session.commit()
        
        # 6. User Progress
        for user in user_objs:
            if user.is_approved:
                # Random progress for some courses
                for course in course_objs[:2]:
                    for lesson in course.lessons:
                        if lesson.order == 1:
                            up = UserLessonProgress.query.filter_by(user_id=user.id, lesson_id=lesson.id).first()
                            if not up:
                                up = UserLessonProgress(user_id=user.id, lesson_id=lesson.id, status='completed', started_at=datetime.utcnow() - timedelta(days=1), completed_at=datetime.utcnow())
                                db.session.add(up)
        db.session.commit()
        
        # 7. Forum
        for course in course_objs[:2]:
            topic = ForumTopic.query.filter_by(title=f"Discussion on {course.title}").first()
            if not topic:
                topic = ForumTopic(title=f"Discussion on {course.title}", content="Let's discuss the concepts learned in this course.", user_id=user_objs[0].id, course_id=course.id)
                db.session.add(topic)
                db.session.flush()
                
                reply = ForumReply(content="I found the second lesson particularly interesting!", user_id=user_objs[1].id, topic_id=topic.id)
                db.session.add(reply)
        db.session.commit()
        
        print("Dummy data populated successfully!")

if __name__ == "__main__":
    populate()
