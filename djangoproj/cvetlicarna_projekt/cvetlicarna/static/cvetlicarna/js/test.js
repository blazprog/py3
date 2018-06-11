/**
 * Created by blazko on 18.6.2015.
 */
$(document).ready(function() {
    solution = ['c1','c2','c3','c4'];
    $('.circle').data('original', true);
    $('.circle').draggable(
        {
        cursor: 'pointer',
        helper: 'clone',
        revert: false,
        start : function(event, ui)
            {
                //ui.helper.draggable( 'option', 'revert', true );
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
            var success = true; //asume success
            for (i=1; i<5; i++) {
                slot_id = 'r' + row + 'c' + i;
                c = $('#slot_id').data('solution');
                if (c != solution[i-1]) {
                    success=false;
                }
                if (success) {
                    alert('You did it!');
                }
            }

        } //end drop
        });


}); // end ready