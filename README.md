This is a JVM build tool, that will compile using:
* Apache Maven
* Gradle
* SBT

Each tool can be used to build you're project simply by 
setting the build_type in the request to the corresponding 
tool (as described above).

Author: $LiM

Demo POST request:
{
    "build_type": "gradle",
    "git_url": "https://github.com/spring-guides/gs-gradle.git",
    "branch": "master",
    "transactionId": "55a0ec45-ad52-4d53-8674-f8843e44c85e",
    "boxId": "946ffda8-1674-4663-b3a2-ab204908d64b",
    "run_script_path": "\\initial\\build.gradle",
    "environment": "dev"
}
