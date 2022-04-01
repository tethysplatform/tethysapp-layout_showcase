window.addEventListener('load', function() { // wait for page to load
    let selection_interaction = TETHYS_MAP_VIEW.getSelectInteraction();

    // Called each time the select interaction's list of features changes
    selection_interaction.getFeatures().on('change:length', function(e) {
        // Check if there is at least 1 feature selected
        if (e.target.getLength() > 0) {
            // Do something with the feature
            let selected_feature = e.target.item(0); // 1st feature in Collection
            console.log(`Selected State: ${selected_feature.get('name')}`);
        }
    });
});