from ..extensions import db
from ..models.user import User
from ..models.friend import Friend
from ..utils.R import R
from flask import current_app
from flask_login import current_user

def add_friend_service(data):
    """添加好友服务"""
    try:
        friend_id = data.get('friend_id')
        if not friend_id:
            return R.fail(message="缺少friend_id参数", code=400)
        
        if current_user.id == friend_id:
            return R.fail(message="不能添加自己为好友", code=400)
            
        friend = User.query.get(friend_id)
        if not friend:
            return R.fail(message="用户不存在", code=400)
            
        existing = Friend.query.filter_by(
            user_id=current_user.id,
            friend_id=friend_id
        ).first()
        
        if existing:
            return R.fail(message="好友请求已存在", code=400)
            
        new_friend = Friend(
            user_id=current_user.id,
            friend_id=friend_id,
            status='pending'
        )
        db.session.add(new_friend)
        db.session.commit()
        return R.ok(message="好友请求已发送", data=new_friend.to_dict(), code=200)
        
    except Exception as e:
        current_app.logger.error(f"发送好友请求失败: {str(e)}")
        db.session.rollback()
        return R.fail(message="发送好友请求失败", code=500)

def query_friends_service(data):
    """查询已建立的好友关系服务"""
    try:
        friend_id = data.get('friend_id')
        nickname = data.get('nickname')
        
        # ID精确查询处理
        if friend_id:
            # 先检查用户是否存在
            target_user = User.query.get(friend_id)
            if not target_user:
                return R.fail(message="用户不存在")

            # 再验证好友关系
            friend_relation = Friend.query.filter_by(
                user_id=current_user.id,
                friend_id=friend_id,
                status='accepted'
            ).first()

            if not friend_relation:
                return R.fail(message="该用户不是您的好友")

            return R.ok(data=[{
                'friend_id': target_user.id,
                'nickname': target_user.nickname,
                'telephone': target_user.telephone,
                'created_time': target_user.created_time.strftime('%Y-%m-%d %H:%M:%S')
            }])

        # 昵称模糊查询
        base_query = db.session.query(User).join(
            Friend, Friend.friend_id == User.id
        ).filter(
            Friend.user_id == current_user.id,
            Friend.status == 'accepted'
        )

        if nickname:
            base_query = base_query.filter(User.nickname.ilike(f"%{nickname}%"))

        friends = base_query.all()

        return R.ok(
            data=[{
                'friend_id': user.id,
                'nickname': user.nickname,
                'telephone': user.telephone,
                'created_time': user.created_time.strftime('%Y-%m-%d %H:%M:%S')
            } for user in friends],
            message='找到{}条记录'.format(len(friends)) if friends else '未找到匹配好友'
        )

    except Exception as e:
        current_app.logger.error(f"查询好友失败: {str(e)}")
        return R.fail(message="查询好友失败")
