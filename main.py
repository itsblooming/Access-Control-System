from database import create_database, add_user, get_user_id, get_user_behavior_data
from behavior import record_user_behavior
from analysis import analyze_user_behavior as analyze_behavior

def main():
    create_database()
    username = "test_user"
    add_user(username)
    
    user_id = get_user_id(username)
    if user_id is None:
        print(f"No data fetched from the database for user_id: {username}. User does not exist.")
        return
    
    record_user_behavior(username)
    
    data = get_user_behavior_data(user_id)
    print("Fetched data:", data) 
    6
    if not data:
        print(f"No behavior data found for user_id: {user_id}")
        return
    
    analyze_behavior(data)  

if __name__ == "__main__":
    main()
