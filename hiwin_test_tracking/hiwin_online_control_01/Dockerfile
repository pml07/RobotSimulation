# Use the official .NET SDK image as the base image
FROM mcr.microsoft.com/dotnet/sdk:latest AS build

# Set the working directory for your project
WORKDIR /app

# Copy your project files into the Docker container
COPY . .

# Restore NuGet packages and build the project
RUN dotnet restore
RUN dotnet publish -c Release -o out

# Use the official .NET runtime image as the final base image
FROM mcr.microsoft.com/dotnet/runtime:latest AS runtime

# Set the working directory for your application
WORKDIR /app

# Copy the built project files from the build stage
COPY --from=build /app/out .

# Set the default command to run your application
ENTRYPOINT ["dotnet", "hiwin_online_control_01.dll"]
