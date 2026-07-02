@extends('layouts.adminmaster')
@section('content')

<br><br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">District Insert</h4>
                  <p class="card-description">
                    Insert your Location name
                  </p>
                  <form  class="forms-sample"form  action="{{route('updateloctable',$loc->locationid)}}" method="post">
                     @csrf
                    <div class="form-group">
                      <label for="exampleInputName1"> Location Name</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Name" name="locationname" value="{{ $loc->locationname }}">
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