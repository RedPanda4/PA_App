from database import *
from util import *


@app.route('/')
def main():
	return render_template('main.html')


@app.route('/communities', methods=['GET', 'POST'])
def community_f():
	if request.method == 'POST':
		if request.form.get('delete'):
			community_d = Community.get(Community.name == request.form['delete'])
			if not Member.select().where(Member.community_id == community_d.id).count():
				community_d.delete_instance()
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
	return render_template('tables/communities.html', communities=communities)


@app.route('/players', methods=['GET', 'POST'])
def player_f():
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
	return render_template('tables/player.html', players=players, communities=communities)


@app.route('/meetings', methods=['GET', 'POST'])
def meetings_f():
	if request.method == 'POST':
		if request.form.get('date'):
			if (request.form.get('date')) == 'now':
				values = {
					'date': int(datetime.datetime.today().timestamp() * 1000)
				}
			else:
				values = {
					'date': int(datetime.datetime.today().timestamp() * 1000)
				}
			a = Meeting.create(**values)
			s = "/meetings/{0}"
			return redirect(s.format(a.get_id()))
	meetings = Meeting.select()
	return render_template('tables/meeting.html', meetings=meetings)


if __name__ == '__main__':
	app.run()
