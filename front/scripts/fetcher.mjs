export async function fetcher  (url) {
    return await fetch(url).then(data => data.json()).then(result => result)
}