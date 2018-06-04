# Place-O-Mat

Place-O-Mat is a small Flask app that queries various services for a list of locations given some input parameters. Currently the service supports Google Places API, and Yelp Fusion.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The following are needed to run the service
```
Vagrant
vagrant-vbguest
```

### Installing

Install VirtualBox

macOS
```
brew cask install virtualbox
```

Install Vagrant via your preferred way

Ubuntu, I think
```
apt-get install vagrant
```

macOS
```
brew install vagrant 
```

Vagrant vbguest plugin

```
vagrant plugin install vagrant-vbguest
```


## Running the tests

You can run the tests with

```
nosetests -v
```

Currently, only the provider map has a test.

## How to run

Place your Places API and Yelp Fusion keys into the `init.sh`

Use `vagrant up` and then `./run_server_devel.sh`

The Flask app should start, and you should see the `werkzeug` information in your console. Navigate your preferred interface `safari`, `curl`, `Postman`, and send some requests!

For example, I will show a query string here. Note that if you use a tool like Postman, you can give parameters and allow the tool to build the query string.

`curl -x GET localhost:5000/search/yelp/query=cafes+in+sydney`

or
`curl -X GET 'localhost:5000/search/google?query=jimdo+gmbh&location=53,10'`

```json
[
    {
        "Address": "Platz der Republik 1, 11011 Berlin, Germany",
        "Description": "point_of_interest, establishment",
        "ID": "ChIJbVDuQcdRqEcR5X3xq9NSG2Q",
        "Location": [
            52.5186202,
            13.3761872
        ],
        "More Details": {
            "url": "https://maps.google.com/?cid=7213450297240288741",
            "website": "http://www.bundestag.de/kulturundgeschichte/architektur/reichstag/"
        },
        "Name": "Reichstag Building",
        "Provider": "Google Maps"
    }
]
```

## Endpoints

Search for something via `/search/<provider>`, where `provider` is one of `yelp`, `google`.

Hit `/search/all` or `/search` and query for data for _all_ providers.

## Available Parameters

So far, you can use the following parameters

* Query - String to search for, like `cafes` or `Starbucks in Berlin`
* Location - Latitude, Longitude
* Radius - A number of meter around the location to search
* Open - Return things that are currently open

Other parameters specific to the service, e.g. Places API, can be used without strict support, but you are on your own :)

## Errors

The service provides rudimentary validation:

`localhost:5000/search/yelp?query=Starbucks`

```json
{
    "reason": "Must supply latitude and longitude, or location"
}
```
