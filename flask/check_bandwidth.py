# -*- coding: utf-8 -*-
import requests


def check_urls(urls):
    for url in urls:
        playlist = requests.get(url).text.splitlines()
        urls_and_bandwidthes = {}
        for i in playlist:
            if i.startswith('#EXT-X-STREAM-INF'):
                url_index = playlist.index(i) + 1
                for n in i.split(','):
                    if n.startswith('BANDWIDTH'):
                        bandwidth = int(n.split('=')[1])
                relative_variant_url = playlist[url_index]
                urls_and_bandwidthes[relative_variant_url] = bandwidth
        for k in urls_and_bandwidthes:
            if k.startswith('http'):
                playlist_url = k
            else:
                playlist_url = '/'.join(url.split('/')[:-1]) + '/' + k
            for repeats in range(5):
                try:
                    variant_playlist = requests.get(playlist_url).text.splitlines()
                    break
                except requests.exceptions.ConnectionError:
                    pass
            clear_variant_playlist = []
            for b in variant_playlist:
                if b.startswith('#EXTINF') or (('#' in b) is False):
                    clear_variant_playlist.append(b)
            count_of_lines = len(clear_variant_playlist)
            current_extinf = 0
            while current_extinf < count_of_lines - 2:
                extinf = float(clear_variant_playlist[current_extinf].split(':')[1][:-1])
                if clear_variant_playlist[current_extinf + 1].startswith('http'):
                    chunk_url = clear_variant_playlist[current_extinf + 1]
                else:
                    chunk_url = '/'.join(playlist_url.split('/')[:-1]) + '/' + clear_variant_playlist[current_extinf + 1]
                for q in range(5):
                    try:
                        fact_bandwidth = len(requests.get(chunk_url).content) * 8 / extinf
                        break
                    except requests.exceptions.ChunkedEncodingError:
                        with open('result.txt', 'a') as file:
                            file.write(f'{chunk_url} - {requests.exceptions.ChunkedEncodingError}\n')
                        pass
                    except requests.exceptions.ConnectionError:
                        with open('result.txt', 'a') as file:
                            file.write(f'{chunk_url} - {requests.exceptions.ConnectionError}\n')
                        pass
                if fact_bandwidth >= urls_and_bandwidthes[k]:
                    with open('result.txt', 'a') as file:
                        file.write(f'Fact bandwith of segment {chunk_url} is too high!!! It is {fact_bandwidth}, '
                                   f'expected {urls_and_bandwidthes[k]}\n')
                current_extinf += 2
    with open('result.txt', 'a') as file:
        file.write('Done!')


with open('urls.txt', 'r') as urls_file:
    urls_param = urls_file.read().splitlines()

check_urls(urls_param)
