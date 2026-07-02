@extends('layouts.adminmaster')
@section('content')

<br><br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">Category Insert</h4>
                  <p class="card-description">
                    Insert your Category Information
                  </p>
                  <form  class="forms-sample" action="{{route('categoryinsert')}}" method="post" enctype="multipart/form-data">
                     @csrf
                    <div class="form-group">
                      <label for="exampleInputName1"> Category Name</label>
                      <input type="text" class="form-control"  placeholder="Name" name="catname" required>
                      @error('catname')
                                <span class="error-message">{{ $message }}</span>
                            @enderror
                    </div>
                    
                    <div class="form-group">
                      <label for="exampleInputName1"> Image</label>
                      <input type="file" class="form-control"  placeholder="Name" name="image">
                      @error('image')
                                <span class="error-message">{{ $message }}</span>
                            @enderror
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