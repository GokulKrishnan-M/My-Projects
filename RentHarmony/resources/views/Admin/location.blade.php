@extends('layouts.adminmaster')
@section('content')

<br><br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">Location Insert</h4>
                  <p class="card-description">
                    Insert your Location name
                  </p>
                  <form  class="forms-sample"form  action="{{route('location_insert')}}" method="post">
                     @csrf
                      <div class="mb-4">
                      <label for="username" class="inline-block mb-2 ml-1 font-bold text-xs text-slate-700 dark:text-white/80">DISTRICT NAME</label><br>
                      <select class="form-control" name="districtid" id="districtid">
                      <option value="">-- Select District Name --</option>
                       @foreach($dist as $d)
                        <option value="{{ $d->districtid }}">
                            {{ $d->districtname}}
                        </option>
                       @endforeach
                      </select>
                    </div>
                    <div class="form-group">
                      <label for="exampleInputName1"> LOCATION NAME</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Name" name="locationname">
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