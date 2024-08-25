from flask import Flask,jsonify,request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,validate, ValidationError
from sqlalchemy.orm import relationship
from sqlalchemy import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+mysqlconnector://root:password@localhost/video_search_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

def merge_sort(arr):
  if len(arr) > 1:
    mid = len(arr)// 2 
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    merge_sort(left_half)
    merge_sort(right_half)
    
    i = j = k = 0
    
    while i < len(left_half) and j < len(right_half):
      if left_half[i] < right_half[j]:
        arr[k] = left_half[i]
        i += 1
      else:
        arr[k] = right_half[j]
        j += 1
      k += 1
    
    while i < len(left_half):
      arr[k] = left_half[i]
      i += 1
      k += 1
    
    while j < len(right_half):
      arr[k] = right_half[j]
      j+=1
      k += 1

def binary_search(arr,title):
  low = 0
  high = len(arr) - 1 #getting last index
  while low <= high:
    mid = (low + high)//2
    if arr[mid] == title:
      return arr[mid]
    elif arr[mid] < title:
      low = mid + 1
    else:
      high = mid -1
  return -1
#<--------------------------------SQL Table Classes----------------------------------->
class VideoTitles(db.Model):
  __tablename__ = "videos"
  id = db.Column(db.Integer,primary_key=True)
  title = db.Column(db.String(255),nullable=False)

#<--------------------------------Schema Tables--------------------------------------->

class VideoTitleSchema(ma.Schema):
  title = fields.String(required=True)
  class Meta:
    fields=('title', 'id')
    
video_schema = VideoTitleSchema()
videos_schema = VideoTitleSchema(many=True)
#<--------------------------------Home Page------------------------------------------->

@app.route('/')
def home():
  return 'Welcome to Video Finder'



#<--------------------------------End Routes------------------------------------------>

@app.route('/search',methods=['GET'])
def get_video_by_title():
  search_query = request.args.get('query')
  videos = db.session.query(VideoTitles.title)
  titles = [video.title for video in videos]
  merge_sort(titles)
  title_search = binary_search(titles,search_query)
  if title_search != -1:
    video = VideoTitles.query.filter_by(title=title_search).first()
    return video_schema.jsonify(video)
  else:
    return jsonify({"error": "Video not found"}), 404
  
@app.route('/add-video',methods=['POST'])
def create_video():
  try:
    video_data = video_schema.load(request.json)
  except ValidationError as err:
    return jsonify(err.messages), 400
  
  video = VideoTitles(title=video_data['title'])
  db.session.add(video)
  db.session.commit()
  return jsonify({"message": "Video has been added successfully"}), 201

@app.route('/search-all',methods=['GET'])
def get_sorted_videos():
  videos = db.session.query(VideoTitles.title)
  titles = [video.title for video in videos]
  merge_sort(titles)
  sorted_videos = []
  for title in titles:
    video = VideoTitles.query.filter_by(title=title).first()
    sorted_videos.append(video)
  return videos_schema.jsonify(sorted_videos)
    
    
#<------------------------------------------------------------------------------------>

if __name__ == '__main__':
  app.run(debug=True)