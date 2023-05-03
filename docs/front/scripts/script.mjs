import { ORANGE, BLUE, GREEN } from "./colors.mjs";

import { fetcher } from "./fetcher.mjs";
import { removeStorage,setStorage,getStoredAddresses } from "./storage.mjs";
import { hasToRefetchAddresses } from "./utils.mjs";

require(["esri/config", "esri/Map", "esri/views/MapView", "esri/Graphic","esri/layers/GraphicsLayer"], function (esriConfig, Map, MapView, Graphic, GraphicsLayer) {

    const map = new Map({
        basemap: "streets-relief-vector"
    });

    const view = new MapView({
        map: map,
        center: [-122.6424753, 45.51871329999999], // Longitude, latitude
        zoom: 16, // Zoom level
        container: "viewDiv" // Div element
    });

    const graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);

    if(hasToRefetchAddresses()){
        removeStorage();
    }

    const addresses = getStoredAddresses();

    if(!addresses || addresses.length === 0){
        removeStorage();

        let loading = true;
        fetcher("http://34.29.139.119:8000/process_adress").then(addresses => {
            setStorage(addresses)
            loading = false;
            setPointsOnMap(addresses)
        });
    }else{
        setPointsOnMap(addresses)
    }

    function setPointsOnMap(addresses){
        addresses.map((address, i) => {
            var add = address
            setTimeout(() => {
                const pointGraphic = createPoint(add.lng, add.lat, i == 0 ? BLUE : i == addresses.length-1 ? GREEN : ORANGE)
                graphicsLayer.add(pointGraphic); 
            }, 1000*(i+3));
        })
    }
    
    function createPoint(lng, lat, color){
        var point = { type: "point", longitude: lng, latitude: lat }; 
        var simpleMarkerSymbol = { type: "simple-marker", color:color,  outline: { color: [255, 255, 255],  width: 1 } };
        var pointGraphic = new Graphic({ geometry: point, symbol: simpleMarkerSymbol }); 
        return pointGraphic;
    }

});