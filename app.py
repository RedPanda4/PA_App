from flask import *
from database import *

app = Flask(__name__)


@app.route('/')
def main():
	return render_template('main.html')


@app.route('/communities', methods=['GET', 'POST'])
def community():
	if request.method == 'POST':
		if request.form.get('delete'):
			community = Community.get(Community.name == request.form['delete'])
			if not Member.select().where(Member.community_id == community.id).count():
				community.delete_instance()
		else:
			values = {
				'name': request.form['name'],
				'color': request.form['color']
			}
			Community.create(**values)
	communities = Community.select().dicts()
	for community in communities:
		member = Member.select().where(Member.community_id == community['id']).count()
		community['deletable'] = not member
	return render_template('communities.html', communities=communities)


@app.route('/players', methods=['GET', 'POST'])
def player():
	if request.method == 'POST':
		if request.form.get('delete'):
			c = Member.get(Member.name == request.form['delete'])
			c.delete_instance()
		else:
			values = {
				'name': request.form['name'],
				'community_id': request.form['community']
			}
			Member.create(**values)
	players = Member.select(Member, Community).join(Community)
	communities = Community.select()
	return render_template('player.html', players=players, communities=communities)


if __name__ == '__main__':
	app.run(debug=True)
