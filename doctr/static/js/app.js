var lastParagraphId;

function highlightSpecificText(event) {
    var paragraphId = event.target.closest('.list-group-item-action').id;
    console.log(paragraphId);
    if (event.target.closest('.list-group-item-action').classList.contains('background-highlight')) {
        //Reset Select
        document.querySelector(`.list-group > #${lastParagraphId}`).classList.remove('background-highlight');
        //Reset Text
        document.querySelectorAll(".main-document > *").forEach(para => {
            para.classList.remove("text-highlight");
            para.classList.remove("text-muted");
        });
    }
    else {
        //Alter Select
        if (typeof lastParagraphId !== 'undefined') {
            document.querySelector(`.list-group > #${lastParagraphId}`).classList.remove('background-highlight');
        }
        event.target.closest('.list-group-item-action').classList.add('background-highlight')

        //Alter Text
        // highlight target paragraph
        var paragraphToBeHighlighted = document.querySelector(`.main-document > #${paragraphId}`);
        paragraphToBeHighlighted.classList.remove("text-muted");
        paragraphToBeHighlighted.classList.add("text-highlight");

        // mute all other paragraphs
        var paragraphsToBeGrey = document.querySelectorAll(`.main-document > :not(#${paragraphId})`);
        paragraphsToBeGrey.forEach(para => {
            para.classList.remove("text-highlight");
            para.classList.add("text-muted");
        });
    }
    //Store last target event id
    lastParagraphId = paragraphId;
}

document.querySelectorAll('.list-group').forEach(item => {
    item.addEventListener('click', highlightSpecificText, false);
});