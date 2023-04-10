// fetch data from external APIs

const getStream = async (provider, sport, query) => {

    apiUrl = 'https://p8q5t9dto5.execute-api.us-east-2.amazonaws.com/default/sportsWiz';

    return fetch(apiUrl + '?' + new URLSearchParams(
        {
            provider: provider,
            sport: sport,
            query: query,
        }
    ),
        {
            'method': 'POST',
        }
    )
        .then(response => response.json())
        .catch(error => console.warn(error))
};
