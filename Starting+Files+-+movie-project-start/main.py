from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from movie import db, Movie, app
from form import RateMovieForm, AddMovieForm
from api_movie import ApiMovie

app.config['SECRET_KEY'] = ''
Bootstrap(app)


@app.route("/")
def home():
    movie_id = request.args.get('id')
    if movie_id:
        movies = ApiMovie()
        movie_details = movies.get_data_details(movie_id)
        title = movie_details["original_title"]
        img_url = f'https://image.tmdb.org/t/p/w500{movie_details["poster_path"]}' # Is completed url image
        year = movie_details["release_date"][:4]
        description = movie_details["overview"]
        new_movie = Movie(title=title, img_url=img_url, year=year, description=description)
        db.session.add(new_movie)
        db.session.commit()

        movie_to_update = Movie.query.filter_by(title=title).first()
        return redirect(url_for('edit', id=movie_to_update.id))

    all_movies = update_ranking()
    return render_template("index.html", all_movies=all_movies)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    """Esta función permite editar el rating o review de una pelicula en la base de datos
        para luego ser mostrada en el website"""
    form = RateMovieForm()

    if form.validate_on_submit():
        movie_id = request.args.get('id')
        movie_to_update = Movie.query.get(movie_id)
        rating = form.rating.data
        review = form.description.data
        movie_to_update.rating = rating
        movie_to_update.review = review
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form)


@app.route("/delete")
def delete():
    """Esta función elimina una pelicula en la base de datos y posteriomente se actualiza en el website"""
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["GET", "POST"])
def add():
    """Esta función permite agregar una pelicula en la base de datos para posteriormente ser mostrata en el website"""
    form = AddMovieForm()
    if form.validate_on_submit():
        movie = form.movie_title.data
        movies = ApiMovie()
        title_movies = movies.get_data(movie)
        return render_template("select.html", title_movies=title_movies)
    return render_template("add.html", form=form)


def update_ranking():
    """Esta función permite actualizar el ranking en la base de datos, luego se mostraran segun la que tenga mas rating"""
    new_order_movie = Movie.query.order_by(Movie.rating).all()
    new_order_movie.reverse()
    count = 1
    for movie in new_order_movie:
        movie.ranking = count
        db.session.commit()
        count += 1
    return new_order_movie

    
if __name__ == '__main__':
    app.run(debug=True)
