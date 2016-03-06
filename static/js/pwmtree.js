/**
 * Client side functionality for
 * sending requests to toggle a setting
 */

var PwmTree = PwmTree || {};

PwmTree.checkin = function( task ){

  $.ajax({
      url: "/worker/" + task,
      type: "GET",
      contentType: "application/x-www-form-urlencoded; charset=utf-8",
      //dataType: "json",
      //data: { title: task },
      success: function (data, textStatus, jqXHR) {
          //alert("success: " + textStatus);
      },
      error: function(jqXHR, textStatus, errorThrown){
          //alert("error: " + textStatus);
      }
   }).done(function (data, textStatus, jqXHR) {

   }).always( function( ){

   });
};

$(document).ready(function( ){
    $('#LightsOnButton').click( function(){ PwmTree.checkin('LightsOn'); });
    $('#DimLightsButton').click(function () { PwmTree.checkin('DimLights'); });
    $('#VeryDimLightsButton').click(function () { PwmTree.checkin('VeryDimLights'); });
    $('#BlinkLightsButton').click(function () { PwmTree.checkin('BlinkLights'); });
    $('#PingPongButton').click(function () { PwmTree.checkin('PingPong'); });
    $('#LightsOffButton').click( function () { PwmTree.checkin('LightsOff'); });
    $('#TrainSlowButton').click(function () { PwmTree.checkin('TrainSlow'); });
    $('#TrainFastButton').click(function () { PwmTree.checkin('TrainFast'); });
    $('#TrainStopButton').click( function () { PwmTree.checkin('TrainStop'); });
    $('#TrainReverseButton').click(function () { PwmTree.checkin('TrainReverse'); });
});