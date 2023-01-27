import requests
import json
import datetime as dt
# colors.pyからカラーコードをインポート
import colors

futon_pick_up_url = "https://public.openrec.tv/external/api/v5/users/indegnasen/pickup-movies"
# 開発中のため取得元動画リンクを固定(ov82wjkex8w<-ここ)
comment_base_url_1 = "https://public.openrec.tv/external/api/v5/movies/ov82wjkex8w/chats?to_created_at="
comment_base_url_2 = ".000Z&is_including_system_message=true"
latest_stream_file_name = "latest_stram.json"
comment_file_name = "comments.json"

# 配信中の動画を取得してlatest_stream.jsonに保存する
def get_latest_stream():
    try:
        response = requests.get(futon_pick_up_url)
        response = response.json()
        with open(latest_stream_file_name, 'w') as f:
            json.dump(response, f, indent=2)
        status = colors.status_ok + " Get latest stream list."
    except Exception as e:
        status = colors.status_error + " Get latest stream list.\n" + str(e)
    return status

# 配信の開始日時を取得
def get_stream_start_time(latest_stream_file_name_def):
    try:
        with open(latest_stream_file_name_def, 'r') as f:
            response = json.load(f)
        stream_start_time_def = response["movies"][0]["published_at"]
        status = colors.status_ok + " Get stream start time. result: " + stream_start_time_def
        # +09:00を削除
        stream_start_time_def_to_datetime = stream_start_time_def.replace("+09:00", "")
        return stream_start_time_def_to_datetime
    except Exception as e:
        status = "[Error] Get stream start time."
        print(colors.status_error + " Get stream start time.\n" + str(e))
        return status

# 配信中のコメントを取得
def get_stream_comments(time_def, comment_base_url_1_def, comment_base_url_2_def, comment_file_name_def):
    try:
        response = requests.get(comment_base_url_1_def + time_def + comment_base_url_2_def)
        response = response.json()
        with open(comment_file_name_def, 'w') as f:
            json.dump(response, f, indent=2)
        status = colors.status_ok + " Get stream comments."
    except Exception as e:
        status = colors.status_error + " Get stream comments.\n" + str(e)
    return status

if __name__ == "__main__":
    print(get_latest_stream())
    stream_start_time = get_stream_start_time(latest_stream_file_name)
    # コメント取得前に配信開始時刻が正常に取得できているか確認
    if stream_start_time != "[Error] Get stream start time.":
        print(colors.status_ok + " Get stream start time.")
        print(get_stream_comments(stream_start_time, comment_base_url_1, comment_base_url_2, comment_file_name))
