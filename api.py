# import openai

# # bp = Blueprint('api',__name__,url_prefix="/")

# # @bp.route('/chat_api',methods=['GET','POST'])
# def chat_api(question):
#     key = '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'
#     openai.api_key = key
#     response = openai.completions.create(
#         model='text-davinci-003',
#         prompt=rf'{question}'
#     )
#     return response.choice[0].text
    
# print(chat_api('很好'))