$(function() {  // wait for page to load
    // Feature Selection Event Handler
    let selection_interaction = TETHYS_MAP_VIEW.getSelectInteraction();

    // Called each time the select interaction's list of features changes
    if (selection_interaction) {
        selection_interaction.getFeatures().on('change:length', function(e) {
            // Check if there is at least 1 feature selected
            if (e.target.getLength() > 0) {
                // 1st feature in collection
                let selected_feature = e.target.item(0);
                // log the value of name property
                console.log(`Selected State: ${selected_feature.get('name')}`); 
            }
        });
    }

    // Map Click Event Handler
    TETHYS_MAP_VIEW.mapClicked(function(coords) {
        let popup_content = document.querySelector("#properties-popup-content");
        let lat_lon = ol.proj.transform(coords, 'EPSG:3857', 'EPSG:4326');
        let rounded_lat = Math.round(lat_lon[1] * 1000000) / 1000000;
        let rounded_lon = Math.round(lat_lon[0] * 1000000) / 1000000;
        popup_content.innerHTML = `<b>Coordinates:</b><p>${rounded_lat}, ${rounded_lon}</p>`;
    });
});