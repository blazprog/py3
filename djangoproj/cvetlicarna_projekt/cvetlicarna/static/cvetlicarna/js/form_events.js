$(document).ready(function() {

    $(".sifraArtikla").change(function()
        {
            var sifraArtikla = $(this).val();
            var url = "/cvetlicarna/get_artikel_details/"
            var params = {"sifraArtikla": sifraArtikla};
            var idWidget = $(this).attr("id")
            var idWidgetCena = idWidget.replace("sifraArtikla", "cena");
            var idWidgetKolicina = idWidget.replace("sifraArtikla", "kolicina");
            var idWidgetDDV = idWidget.replace("sifraArtikla", "idDDV");
            var idWidgetEm = idWidget.replace("sifraArtikla", "idEm");
            var idWidgetPopust = idWidget.replace("sifraArtikla","popust");

            function show_artikel_details(data) {
                var cena = data.cena;
                var idEm = data.idEm;
                var idDDV = data.idDDV;
                $("#" + idWidgetCena).val(cena);
                $("#" + idWidgetKolicina).val(1);
                $("#" + idWidgetDDV).val(idDDV);
                $("#" + idWidgetEm).val(idEm);
                $("#" + idWidgetPopust).val(0);
            };
            $.get(url,params,show_artikel_details);

        }
    )
})




