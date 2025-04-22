from starlette_admin.contrib.sqla import Admin

from app.database import engine
from app.models import User, Game, Question, Participation, Submission, Option, Topic
from app.admin.views import UserView, GameView, TopicView, OptionView, QuestionView, ParticipationView, SubmissionView
# from app.admin.auth import JSONAuthProvider


admin = Admin(
    engine=engine,
    title="bilimdon admin",
    # auth_provider=JSONAuthProvider(login_path="/login", logout_path="/logout"),
)

admin.add_view(UserView(User, icon="fa fa-user"))
admin.add_view(GameView(Game, icon="fa fa-Game"))
admin.add_view(QuestionView(Question, icon="fa fa-Question"))
admin.add_view(ParticipationView(Participation, icon="fa fa-Participation"))
admin.add_view(SubmissionView(Submission, icon="fa fa-Submission"))
admin.add_view(OptionView(Option, icon="fa fa-Option"))
admin.add_view(TopicView(Topic, icon="fa fa-Topic"))


