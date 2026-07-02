@extends('layouts.adminmaster')
@section('content')

<br><br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">District Insert</h4>
                  <p class="card-description">
                    Insert your district name
                  </p>
                  <form  class="forms-sample"form  action="{{route('district_insert')}}" method="post">
                     @csrf
                    <div class="form-group">
                      <label for="exampleInputName1"> District Name</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Name" name="districtname">
                    </div>
                    
                    <button type="submit" class="btn btn-primary mr-2">Submit</button>
                   
                  </form>
                   @if (session('success'))
                  <script>
                    alert('{{session('success') }}')
                  </script>
                  @endif
                </div>
              </div>
            </div>

            @endsection