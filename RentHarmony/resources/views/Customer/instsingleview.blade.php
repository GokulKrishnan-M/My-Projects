@extends('layouts.customermaster')
@section('content')
<style>
    body{background-color: #fcf5f5ff}.card{border:none}.product{background-color: #fff4f4ff}.brand{font-size: 13px}.act-price{color:red;font-weight: 700}.dis-price{text-decoration: line-through}.about{font-size: 14px}.color{margin-bottom:10px}label.radio{cursor: pointer}label.radio input{position: absolute;top: 0;left: 0;visibility: hidden;pointer-events: none}label.radio span{padding: 2px 9px;border: 2px solid #ff0000;display: inline-block;color: #ff0000;border-radius: 3px;text-transform: uppercase}label.radio input:checked+span{border-color: #ff0000;background-color: #ff0000;color: #fff}.btn-danger{background-color: #ff0000 !important;border-color: #ff0000 !important}.btn-danger:hover{background-color: #da0606 !important;
    border-color: #da0606 !important}.btn-danger:focus{box-shadow: none}.cart i{margin-right: 10px}
</style>
<script>
    function change_image(image){

                 var container = document.getElementById("main-image");

                container.src = image.src;
            }
    


            document.addEventListener("DOMContentLoaded", function(event) {



            



            });
</script>
<br><br>
<div class="container mt-5 mb-5">
    <div class="row d-flex justify-content-center">
        <div class="col-md-10">
            <div class="card">
                <div class="row">
                    <div class="col-md-6">
                        <div class="images p-3">
                            <div class="text-center p-4"> <img id="main-image" src="{{ asset('/uploads/' . $instruments->image) }}" width="700" style="height:630px;"/> </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="product p-4">
                           
                                <h5 class="text-uppercase">{{ $instruments->instname }}</h5>
                                <div class="price d-flex flex-row align-items-center"> <span class="act-price">₹{{ $instruments->ppd }}</span>
                                    
                                </div>
                            </div>
                            <p class="about">{{ $instruments->desc }}</p>
                             <p class="about">stock:{{ $instruments->stock }}</p>
                            <div class="cart mt-4 align-items-center"> <a href="{{route('booking' , ['instid' => $instruments->instid])}}" class="btn btn-danger text-uppercase mr-2 px-4"> BOOK NOW</a> </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<br><br>
 @endsection
