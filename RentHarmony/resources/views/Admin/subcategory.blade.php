@extends('layouts.adminmaster')
@section('content')

<br><br>
<div class="col-12 grid-margin stretch-card">
              <div class="card">
                <div class="card-body">
                  <h4 class="card-title">Subcategory Insert</h4>
                  <p class="card-description">
                    Insert your Category Information
                  </p>
                  <form  class="forms-sample"form  action="{{route('subcatinsert')}}" method="post" enctype="multipart/form-data">
                     @csrf
                      <div class="mb-4">
                      <label for="username" class="inline-block mb-2 ml-1 font-bold text-xs text-slate-700 dark:text-white/80">SUBCATEGORY NAME</label><br>
                      <select class="form-control" name="catid">
                      <option value="">-- Select Category Name --</option>
                       @foreach($subcat as $d)
                        <option value="{{ $d->catid }}">
                            {{ $d->catname}}
                        </option>
                       @endforeach
                      </select>
                    </div>
                    <div class="form-group">
                      <label for="exampleInputName1"> CATEGORY NAME</label>
                      <input type="text" class="form-control" id="exampleInputName1" placeholder="Name" name="subcatname">
                      @error('subcatname')
                                <span class="error-message">{{ $message }}</span>
                            @enderror
                    </div>
                    <div class="form-group">
                      <label for="exampleInputName1"> Image</label>
                      <input type="file" class="form-control"  placeholder="Name" name="subimage">
                      @error('subimage')
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