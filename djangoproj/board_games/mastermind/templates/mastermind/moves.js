/*
 * Funkcije, ki se v glavnem ukvarjajo s premikanjem krogov na plosco in
 * z javljanjem rezultatov
 */

$(document).ready(function() {
    solution = ['c1','c2','c3','c4'];
    $('.row').data('solution','EMPTY-SLOT'); //to mark empty slot 
    $('.circle').data('original', true);
    $('.circle').draggable(
        {
        cursor: 'pointer',
        helper: 'clone',
        revert: false,
        start : function(event, ui) 
            {
                ui.helper.css('background-color',$('#' + event.target.id).css('background-color'));
                //ui.helper.css('background-color','green');
            },
        }
    );
    
    $('.row').droppable(
        {
        drop: function(event, ui) 
        {
            if (!ui.draggable.data('original')) {
                ui.draggable.draggable( 'option', 'revert', false );
                $(ui.draggable).position( { of: $(this), my: 'ceneter', at: 'center' } );
                }
            else {
                clone = $(ui.draggable).clone();
                $(this).append(clone);
                clone.draggable({
                    helper: 'original',
                    revert: true,    
                });
                //clone.draggable( 'option', 'revert', false );
                clone.position( { of: $(this), my: 'ceneter', at: 'center' } );
            //}

            }
            var id = ui.draggable.attr('id');
            $(this).data('solution', id);
            var slot_id = $(this).attr('id');
            var row = slot_id[1];
            var col = parseInt(slot_id[3]); //slots have format rncn, row nunber is on 3nd position
            blacks = 0;
            whites = 0;
            for (i=1; i<5; i++) {
                slot_id = 'r' + row + 'c' + i;
                c = $('#' + slot_id).data('solution');
                if (c == 'EMPTY-SLOT') { return; } //niso še štiri v vrsto ne rabim nicesar javljat 
                pos = solution.indexOf(c); 
                if (pos != (-1)) {
                    if (pos == i-1) { //če je na istem mesti v vrstici, kot v rešitvi
                        blacks++;
                    }
                    else {
                        whites++;
                    }
                }
            }
            showHints(blacks, whites,row);
            if (blacks == 4) {
                alert('You did it!');
            }

        } //end drop
        });
   
        function showHints(blacks, whites,row) {
            var parent = 'r' + row + 'c5';
            var hint_num = 0;
            for (var i=0; i< blacks; i++) {
                hint_num ++;
                var selector = '#' + parent + ' #hint' + hint_num.toString();
                $(selector).addClass('black-circle');
            }

            for (i=0; i< whites; i++) {
                hint_num ++;
                var selector = '#' + parent + ' #hint' + hint_num.toString();
                $(selector).addClass('white-circle');
                
            }

        }
    
}); // end
