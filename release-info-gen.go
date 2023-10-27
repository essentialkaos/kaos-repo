package main

// ////////////////////////////////////////////////////////////////////////////////// //
//                                                                                    //
//                         Copyright (c) 2021 ESSENTIAL KAOS                          //
//      Apache License, Version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>     //
//                                                                                    //
// ////////////////////////////////////////////////////////////////////////////////// //

import (
	"fmt"
	"os"
	"os/exec"
	"sort"
	"strconv"
	"strings"

	"pkg.re/essentialkaos/ek.v12/fmtc"
	"pkg.re/essentialkaos/ek.v12/path"
	"pkg.re/essentialkaos/ek.v12/sortutil"
	"pkg.re/essentialkaos/ek.v12/strutil"
)

// ////////////////////////////////////////////////////////////////////////////////// //

const (
	APP  = "ReleaseInfoGen"
	VER  = "1.0.0"
	DESC = "Go utility for generating release info"
)

const (
	TYPE_ADDED    = "A"
	TYPE_MODIFIED = "M"
	TYPE_DELETED  = "D"
	TYPE_RENAMED  = "R"
)

// ////////////////////////////////////////////////////////////////////////////////// //

type Change struct {
	Type       string
	File       string
	Source     string
	Similarity float64
}

type Changes []Change

func (c Changes) Len() int      { return len(c) }
func (c Changes) Swap(i, j int) { c[i], c[j] = c[j], c[i] }
func (c Changes) Less(i, j int) bool {
	return sortutil.NaturalLess(
		strings.ToLower(c[i].File),
		strings.ToLower(c[j].File),
	)
}

// ////////////////////////////////////////////////////////////////////////////////// //

func main() {
	checkoutLatestChanges()
	changes := createChangesList()

	listAdditions(changes)
	listModifications(changes)
	listDeletions(changes)
}

// ////////////////////////////////////////////////////////////////////////////////// //

// checkoutLatestChanges checkouts the latest changes
func checkoutLatestChanges() {
	cmd := exec.Command("git", "checkout", "-B", "master", "origin/master")
	err := cmd.Run()

	if err != nil {
		printErrorAndExit(err.Error())
	}

	cmd = exec.Command("git", "checkout", "develop")
	err = cmd.Run()

	if err != nil {
		printErrorAndExit(err.Error())
	}
}

// createChangesList makes slice with changes between develop and master branch
func createChangesList() Changes {
	cmd := exec.Command("git", "diff", "--name-status", "master")
	output, err := cmd.Output()

	if err != nil {
		printErrorAndExit(err.Error())
	}

	var changes Changes

	for _, line := range strings.Split(string(output), "\n") {
		if strings.Trim(line, " ") == "" {
			continue
		}

		changes = append(changes, parseChangeInfo(line))
	}

	changes = filterChanges(changes)

	sort.Sort(changes)

	return changes
}

// listAdditions prints list with new specs
func listAdditions(changes Changes) {
	var data []string

	for _, c := range changes {
		if c.Type == TYPE_ADDED {
			pkgName := getSpecValue(c.File, "name")
			pkgDesc := getSpecValue(c.File, "summary")

			data = append(data, fmt.Sprintf(
				"`%s` (_%s_)", pkgName, pkgDesc,
			))
		}

		if c.Type == TYPE_RENAMED {
			fileName := path.Base(c.File)
			srcName := path.Base(c.Source)

			if fileName != srcName {
				pkgName := getSpecValue(c.File, "name")
				pkgDesc := getSpecValue(c.File, "summary")

				data = append(data, fmt.Sprintf(
					"`%s` (_%s_)", pkgName, pkgDesc,
				))
			}
		}
	}

	sortutil.StringsNatural(data)

	fmt.Println("### New packages\n")

	for _, info := range data {
		fmt.Printf("- %s\n", info)
	}

	fmtc.NewLine()
}

// listModifications prints list with updated specs
func listModifications(changes Changes) {
	var data []string

	for _, c := range changes {
		if c.Type != TYPE_MODIFIED {
			continue
		}

		pkgName := getSpecValue(c.File, "name")
		pkgVer := getSpecValue(c.File, "version")

		data = append(data, fmt.Sprintf(
			"`%s` updated to %s", pkgName, pkgVer,
		))
	}

	sortutil.StringsNatural(data)

	fmt.Println("### Updates\n")

	for _, info := range data {
		fmt.Printf("- %s\n", info)
	}

	fmtc.NewLine()
}

// listDeletions prints list with deleted specs
func listDeletions(changes Changes) {
	var data []string

	for _, c := range changes {
		if c.Type == TYPE_DELETED {
			dirName := path.Base(path.Dir(c.File))
			fileName := path.Base(c.File)
			pkgName := strutil.Exclude(fileName, ".spec")

			if isUniqSpec(c.File) {
				data = append(data, pkgName)
			} else {
				data = append(data, dirName+"/"+pkgName)
			}
		}

		if c.Type == TYPE_RENAMED {
			fileName := path.Base(c.File)
			srcName := path.Base(c.Source)

			if fileName != srcName {
				pkgName := strutil.Exclude(srcName, ".spec")
				dirName := path.Base(path.Dir(c.Source))

				if isUniqSpec(c.File) {
					data = append(data, pkgName)
				} else {
					data = append(data, dirName+"/"+pkgName)
				}
			}
		}
	}

	sortutil.StringsNatural(data)

	fmt.Println("### Deletions\n")

	for _, pkg := range data {
		fmt.Printf("- `%s`\n", pkg)
	}

	fmtc.NewLine()
}

// parseChangeInfo parses change info
func parseChangeInfo(line string) Change {
	changeType := strutil.ReadField(line, 0, true, " ", "\t")

	switch changeType {
	case TYPE_ADDED, TYPE_DELETED, TYPE_MODIFIED:
		return Change{
			Type: changeType,
			File: strutil.ReadField(line, 1, true, " ", "\t"),
		}
	}

	if !strings.HasPrefix(line, TYPE_RENAMED) {
		return Change{}
	}

	return Change{
		Type:       TYPE_RENAMED,
		File:       strutil.ReadField(line, 2, true, " ", "\t"),
		Source:     strutil.ReadField(line, 1, true, " ", "\t"),
		Similarity: extractSimilarityIndex(changeType),
	}
}

// extractSimilarityIndex extracts similarity index from record
func extractSimilarityIndex(data string) float64 {
	data = strings.TrimLeft(data, TYPE_RENAMED+"0")
	v, _ := strconv.ParseFloat(data, 64)
	return v / 100
}

// filterChanges removes all non-spec changes from given slice
func filterChanges(changes Changes) Changes {
	var index int

	for _, c := range changes {
		if strings.HasSuffix(c.File, ".spec") {
			changes[index] = c
			index++
		}
	}

	return changes[:index]
}

// getSpecValue reads macro value from spec
func getSpecValue(file, macro string) string {
	cmd := exec.Command("rpm", "-q", "--qf", "%{"+macro+"}\n", "--specfile", file)
	output, err := cmd.Output()

	if err != nil {
		return ""
	}

	return strings.Split(string(output), "\n")[0]
}

// isUniqSpec returns true if spec is unique (only one spec with this name)
func isUniqSpec(file string) bool {
	switch {
	case strings.Contains(file, "postgres"):
		return false
	}

	return true
}

// ////////////////////////////////////////////////////////////////////////////////// //

// printError prints error message to console
func printError(f string, a ...interface{}) {
	if len(a) == 0 {
		fmtc.Fprintln(os.Stderr, "{r}"+f+"{!}")
	} else {
		fmtc.Fprintf(os.Stderr, "{r}"+f+"{!}\n", a...)
	}
}

// printError prints warning message to console
func printWarn(f string, a ...interface{}) {
	if len(a) == 0 {
		fmtc.Fprintln(os.Stderr, "{y}"+f+"{!}")
	} else {
		fmtc.Fprintf(os.Stderr, "{y}"+f+"{!}\n", a...)
	}
}

// printErrorAndExit print error mesage and exit with exit code 1
func printErrorAndExit(f string, a ...interface{}) {
	printError(f, a...)
	os.Exit(1)
}
