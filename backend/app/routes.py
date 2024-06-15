from flask import Blueprint, request, jsonify, abort, send_file
import redis
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def hello():
    return "Hello, World!"

@bp.route('/generate-cover-letter-task', methods=['POST'])
def generate_cover_letter_task():
    from .app import crew_write_cover_letter_task
    session_id = request.headers.get('x-session-id')
    job_url = request.form['jobUrl']
    linkedin_url = request.form['linkedinUrl']
    resume_file = request.files['resumeFile']
    
    print(job_url)
    print(linkedin_url)
    print(resume_file)
    # create data directory for the session (if they don't already exist)
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/' + session_id):
        os.mkdir('data/' + session_id)
        os.mkdir('data/' + session_id + '/input')
        os.mkdir('data/' + session_id + '/output')
    # save resume file to local directory (if it doesn't already exist)
    # resume_file_path = os.path.join('data/' + session_id + '/input', resume_file.filename)
    # print('resume file path: ', resume_file_path)
    # if not os.path.exists(resume_file_path):
    #     resume_file.save(resume_file_path)

    # Here you would include your agent definitions and processing logic
    task = crew_write_cover_letter_task.apply_async(args=[job_url, linkedin_url,"",""])
                                                        #   resume_file_path, session_id
                                                        #   ])

    return jsonify({'task_id': task.id})

@bp.route('/status/<task_id>')
def task_status(task_id):
    from .app import celery
    print("Status endpoint hit! Task ID: ", task_id)
    task = celery.AsyncResult(task_id)
    try:
        print("Task state: ", task.state)
    except Exception as e:
        print("Task state error: ", str(e))
        return jsonify({'error': 'Could not retrieve task state', 'details': str(e)}), 500
        
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state == 'REVOKED':
        response = {
            'state': task.state,
            'status': 'Task cancelled!'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('status', ''),
            'result': task.info.get('result', '') if task.state == 'SUCCESS' else ''
        }
    else:
        response = {
            'state': task.state,
            'status': task.info.get('exec_message', str(task.info))  # Exception raised
        }
        print("FAILURE:", response)
    return jsonify(response)

@bp.route('/cancel-task/<task_id>', methods=['POST'])
def cancel_task(task_id):
    from .app import celery
    print("Cancel endpoint hit! Task ID: ", task_id)
    celery.control.revoke(task_id, terminate=True, signal='SIGKILL')
    
    return jsonify({'status': 'Task cancelled!'})

@bp.route('/download/<session_id>/<file_name>', methods=['GET'])
def download(session_id, file_name):
    print("Download endpoint hit! Session ID: ", session_id, "File name: ", file_name)
    
    # Construct absolute path
    directory = os.path.abspath(os.path.join('data', session_id, 'output'))
    file_path = os.path.join(directory, file_name)
    print("Absolute directory: ", directory)
    print("Absolute file path: ", file_path)
    
    try:
        if os.path.exists(file_path):
            print("File found!")
            return send_file(file_path, as_attachment=True)
        else:
            print("File not found!")
            abort(404)
    except Exception as e:
        print(f"Error occurred: {e}")
        abort(500, description="Internal Server Error")

# Test Redis connection
@bp.route('/test_redis')
def test_redis():
    try:
        r = redis.from_url(os.getenv('REDIS_URL'))
        r.ping()
        return jsonify({"status": "success", "message": "Connected to Redis successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# todo: This is a temporary route for testing without Celery. We will remove this later.
# @bp.route('/generate-cover-letter', methods=['POST'])
# def generate_cover_letter():
#     # from .crew_ai import crew_write_cover_letter
#     job_url = request.form['jobUrl']
#     linkedin_url = request.form['linkedinUrl']
#     resume_file = request.files['resumeFile']
    
#     print(job_url)
#     print(linkedin_url)
#     print(resume_file)
#     # todo: Actually this might not work. We might need to save it to redis or something
#     # save resume file to local directory
#     resume_file_path = os.path.join('data/input', resume_file.filename)
#     resume_file.save(resume_file_path)

#     # Here you would include your agent definitions and processing logic
#     # cover_letter = crew_write_cover_letter(job_url, linkedin_url, resume_file_path)

#     return jsonify({'coverLetter': cover_letter})
