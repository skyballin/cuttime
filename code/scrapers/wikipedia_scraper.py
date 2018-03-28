import pandas as pd
import wikipediaapi
import json

def get_artists(artists):
	all_artists = []
	for artist in artists:    
		if 'Category:' in artist:
			continue
		elif 'Wikipedia' in artist:
			continue
		elif 'Portal:' in artist:
			continue
		elif 'Template:' in artist:
			continue
		elif 'Template talk:' in artist:
			continue
		elif 'List of' in artist:
			continue
		elif artist in genres:
			continue
		else:
			all_artists.append(artist)
	return all_artists

wiki_wiki = wikipediaapi.Wikipedia('en')
genre_exclude_list = ['Template:Music genres', 'Template:Popular music', 
                'Template talk:Music genres', 'Template talk:Popular music', 
                'Category:Opera', 'Category:Pop music genres', 
                'Category:Rhythm and blues music genres', 
                'Category:Traditional music by country', 
                'Portal:Lists', 'Portal:Music',
                '1490s in music', '1500s in music', '1510s in music', 
                '1520s in music', '1530s in music', '1540s in music', 
                '1940s in music', '1950s in music', '1960s in music', 
                '1970s in music', '1980s in music', '1990s in music',
                '2000s in music', '2010s in music', 'Wikipedia']
genre_page = wiki_wiki.page('List_of_popular_music_genres')
genres = list(genre_page.links.keys())
genres = [i for i in genres if i not in genre_exclude_list]

music = []
for g in genres:
	g = g.replace('(music)', '').strip()
	g = g.replace('(music genre)', '').strip()
	g = g.replace('(genre)', '').strip()
	g = g.replace('music', '').strip()
	g = g.replace(' ', '_')

	list_of_link1 = wiki_wiki.page('List_of_'+g+'_musicians')
	list_of_link1a = wiki_wiki.page('List_of_'+g.lower()+'_musicians')

	list_of_link2 = wiki_wiki.page('List_of_'+g+'_artists')
	list_of_link2a = wiki_wiki.page('List_of_'+g.lower()+'_artists')

	category_link1 = wiki_wiki.page('Category:'+g+'_musicians')
	category_link1a = wiki_wiki.page('Category:'+g.lower()+'_musicians')

	category_link2 = wiki_wiki.page('Category:'+g+'_artists')
	category_link2a = wiki_wiki.page('Category:'+g.lower()+'_artists')

	genre = wiki_wiki.page(g)
	if list_of_link1.exists() or list_of_link1a.exists():
		if list_of_link1.exists():
			artists = list(list_of_link1.links.keys())
		else:
			artists = list(list_of_link1a.links.keys())
		artists = get_artists(artists)
		music.append((g, genre.summary, 'List_of_'+g+'_musicians', artists))

	elif list_of_link2.exists() or list_of_link2a.exists():
		if list_of_link2.exists():
			artists = list(list_of_link2.links.keys())            
		else:
			artists = list(list_of_link2a.links.keys())
		artists = get_artists(artists)
		music.append((g, genre.summary, 'List_of_'+g+'_artists', artists))

	elif category_link1.exists() or category_link1a.exists():
		if category_link1.exists():
			artists = list(category_link1.categorymembers.keys())
		else:
			artists = list(category_link1a.categorymembers.keys())
		music.append((g, genre.summary, 'Category:'+g+'_musicians', artists))
	elif category_link2.exists() or category_link2a.exists():
		if category_link1.exists():
			artists = list(category_link2.categorymembers.keys())
		else:
			artists = list(category_link2a.categorymembers.keys())
		music.append((g, genre.summary, 'Category:'+g+'_artists', artists))
	else:
		music.append((g, genre.summary, False, False))

music = pd.DataFrame(music, columns=['genre', 'genre_summary', 'artist_list_page', 'artists'])