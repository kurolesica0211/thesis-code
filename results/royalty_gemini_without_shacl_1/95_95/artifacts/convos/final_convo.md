================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Nicholas Michael de Roumanie Medforth-Mills (born 1 April 1985), formerly known as Prince Nicholas of Romania, is the eldest child and only son of Princess Elena of Romania and Robin Medforth-Mills.
As a grandson of King Michael of Romania, he was third in line to the defunct throne of Romania according to a new family statute enacted in 2007, that also conferred the title of a "prince of Romania" on him which was removed in 2015.
Early life

Birth

Nicholas de Roumanie Medforth-Mills was born on 1 April 1985 at La Tour Hospital in Meyrin, a commuter town near Geneva, Switzerland, the first child and son of Princess Elena of Romania and her first husband Robin Medforth-Mills and the second grandchild of King Michael I of Romania and his wife Queen Anne.
He was baptized in the Orthodox faith, his godparents being Queen Anne (his maternal grandmother) and Crown Princess Margareta of Romania (his maternal aunt).
Childhood

Until the age of four, Medforth-Mills lived with his sister and parents at the Romanian royal family's residence in Versoix, Switzerland.
Medforth-Mills joined the Beaver Scouts at age five.
During his childhood, he developed an interest in cars, an interest shared with his grandfather King Michael I.
During holidays in Versoix, Switzerland, with his maternal grandparents, Nicholas spent hours in his grandfather's garage, watching him maintain his Jeep collection.
In an interview with historian Filip-Lucian Iorga, Nicholas recalled the time spent with King Michael, and how he had been allowed to drive one of his cars, a Ford which once belonged to General George S. Patton; the vehicle was given to his grandfather by Queen Anne's paternal uncle Prince Felix of Bourbon-Parma as a gift.
He also recalled spending time with Queen Anne at Versoix where they used to fish and play golf together.
As a descendant of Queen Victoria of the United Kingdom and King Christian IX of Denmark, he regularly met with many of his extended relatives.
Education

Medforth-Mills attended Argyle House School, Sunderland, England which he left in 1999 with eight GCSEs - English Language, English Literature, Mathematics, Science (Chemistry, Biology and Physics), French, German, Information Technology, and Geography.
Before enrolling for university he took a five-year "Gap year", where:


Activities in Romania

Nicholas’s first major appearance in Romania was on 19 April 1992 on Easter Day along with his grandparents
King Michael
I and Queen Anne and with his mother and her second husband Alexander Nixon.
Nicholas came again for the second time on Christmas Day 1997, when the entire royal family set foot in Romania for the first time after nearly five decades of exile.
In 2002, he visited Romania for the third time; he stayed at Elisabeta Palace.
In 2008, de Roumanie Medforth-Mills became more involved in the public life of Romania, taking part, for instance, at the 2008 UNITER theatre gala and in visits throughout the country with his aunt, Crown Princess Margareta, and  Radu Duda.
Royal status

Prince of Romania

In 1997, Romanian monarchists intended to ask Michael to designate a male heir-presumptive from the House of Hohenzollern in keeping with the rules of the last royal constitution which were based on agnatic primogeniture and Salic law.
The monarchists eventually agreed on a compromise and requested him to designate a male rather than female heir-presumptive, in the person of Nicholas.
However, under the influence of Queen Anne, Michael rejected the monarchists' request, and at the end of 1997, he designated Princess Margareta as heir presumptive in keeping with the European Convention on Human Rights, which meant Nicholas would only succeed to the headship of the royal family after the deaths of King Michael, Crown Princess Margareta and his mother.
In 2005, King Michael told Nicholas that he could choose to have the chance of becoming a "prince of Romania" which would mean assuming responsibility in a conscious manner by starting to work for the country.
On 30 December 2007, the press office of King Michael announced that Nicholas de Roumanie Medforth-Mills would receive the title "prince of Romania" with the style of "royal highness", coming into effect on Nicholas's 25th birthday.
In February 2008, Nicholas stated in an interview with the Romanian daily newspaper Cotidianul that if the Romanian people asked him to become king, he would not refuse.
In September 2012, after his university studies, he moved to Romania to undertake more of the royal family's public activities.
Removal of titles and illegitimate daughter

On 1 August 2015, former King Michael of Romania signed a document removing the title prince of Romania and the qualification of royal highness from his grandson.
Medforth-Mills also has been removed from the line of succession, as defined by his grandfather.
The former king took the decision after considering that Romania needed a ruler marked by modesty and moral principles, respect and thought for others after the "reign and life" of his eldest daughter, Crown Princess Margareta, will have finished.
In issuing the declaration, the former king expressed the hope that "Nicholas will find in future years a suitable way to serve the ideals and use the qualities that God gave him".
Nicholas's mother, Princess Elena, received notification of the former king's decision in a personal letter.
The validity of the document has been challenged by Nicholas who has stated there was no signature whatsoever from King Michael.
The move "stunned Romanians" and "sparked speculation that a jealous relative had sought to edge Nicholas out of the succession."
The exclusion of Nicholas from the royal succession was due to the birth of an illegitimate daughter, from a short relationship with Nicoleta Cîrjan.
Nicholas released a press statement on 18 November 2017 from London about the child.
Point 2 of the Press release stated, that on learning of the pregnancy, "I returned to Romania in November 2015 to resolve the situation with my alleged child.
On 27 May 2019, Nicholas confirmed via a Facebook post that paternity tests had confirmed the illegitimate daughter is his, and that he had assumed legal responsibility for her.
Allegation of assault

On 8 November 2017, during Michael I's final illness, Crown Princess Margareta filed a complaint with Swiss police alleging that Nicholas tried to force his way into his grandfather's home.
It alleged that Nicholas "physically and verbally assaulted" three staff members, while he accused his relatives of trying to stop him seeing his grandfather and discrediting his name.
Nicholas was acquitted of all charges by the court of Nyon in October 2021.
Marriage

Nicholas married civilly in Henley-on-Thames on 6 October 2017 to Alina-Maria Binder (born in Constanța on 26 January 1988).



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (3c83ba0a-ba32-4bb1-b0e3-b7d96fd636ab)
 Call ID: 3c83ba0a-ba32-4bb1-b0e3-b7d96fd636ab
  Args:
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    type: :Man
  AssignClass (011bd70c-46cf-4000-8562-e86e0e843776)
 Call ID: 011bd70c-46cf-4000-8562-e86e0e843776
  Args:
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    type: :Person
  AddLiteral (8b17f0a6-ae13-4fd9-984b-0807013b500c)
 Call ID: 8b17f0a6-ae13-4fd9-984b-0807013b500c
  Args:
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    literal_value: 1985
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (4ca1d947-67f3-45df-8a14-a13e7760bac6)
 Call ID: 4ca1d947-67f3-45df-8a14-a13e7760bac6
  Args:
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    relation: :formerlyKnownAs
    literal_type: xsd:string
    literal_value: Prince Nicholas of Romania
  AssignClass (4008a5b0-ff76-4913-aba1-75363bbdacfd)
 Call ID: 4008a5b0-ff76-4913-aba1-75363bbdacfd
  Args:
    type: :Woman
    source: Princess_Elena_of_Romania
  AssignClass (977fef64-bf20-428c-ab10-8b73cf2e3019)
 Call ID: 977fef64-bf20-428c-ab10-8b73cf2e3019
  Args:
    type: :Person
    source: Princess_Elena_of_Romania
  AssignClass (4313e861-5fa4-411e-a3f7-774745bfc1c7)
 Call ID: 4313e861-5fa4-411e-a3f7-774745bfc1c7
  Args:
    source: Robin_Medforth-Mills
    type: :Man
  AssignClass (b849aaeb-1b13-428f-ba89-de707f6e6782)
 Call ID: b849aaeb-1b13-428f-ba89-de707f6e6782
  Args:
    source: Robin_Medforth-Mills
    type: :Person
  AddTriple (9791c107-3c9b-431d-9570-4fa81f354800)
 Call ID: 9791c107-3c9b-431d-9570-4fa81f354800
  Args:
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    relation: :hasMother
    target: Princess_Elena_of_Romania
  AddTriple (3eb4ee09-5038-4594-a3a8-e7ab38eb4e88)
 Call ID: 3eb4ee09-5038-4594-a3a8-e7ab38eb4e88
  Args:
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    target: Robin_Medforth-Mills
    relation: :hasFather
  AssignClass (f801a27c-45a6-4d56-bebb-5c8024e6208f)
 Call ID: f801a27c-45a6-4d56-bebb-5c8024e6208f
  Args:
    source: King_Michael_I_of_Romania
    type: :Man
  AssignClass (8179af3c-631b-44f8-86d0-e8780073358e)
 Call ID: 8179af3c-631b-44f8-86d0-e8780073358e
  Args:
    source: King_Michael_I_of_Romania
    type: :Person
  AssignClass (a2c1908a-c8f1-476b-bf86-3c4fcdbc9848)
 Call ID: a2c1908a-c8f1-476b-bf86-3c4fcdbc9848
  Args:
    source: Queen_Anne_of_Romania
    type: :Woman
  AssignClass (a6896361-f06e-4ee6-b68c-10144af51843)
 Call ID: a6896361-f06e-4ee6-b68c-10144af51843
  Args:
    source: Queen_Anne_of_Romania
    type: :Person
  AddTriple (fd25803c-03a4-4406-b7d9-59d179647051)
 Call ID: fd25803c-03a4-4406-b7d9-59d179647051
  Args:
    target: King_Michael_I_of_Romania
    relation: :hasFather
    source: Princess_Elena_of_Romania
  AddTriple (0d470968-94b5-45b9-bf5c-65e363b35887)
 Call ID: 0d470968-94b5-45b9-bf5c-65e363b35887
  Args:
    source: Princess_Elena_of_Romania
    relation: :hasMother
    target: Queen_Anne_of_Romania
  AssignClass (eace398a-1e45-4b79-8d94-c46f774a825f)
 Call ID: eace398a-1e45-4b79-8d94-c46f774a825f
  Args:
    source: Crown_Princess_Margareta_of_Romania
    type: :Woman
  AssignClass (9ff2973e-3061-4d21-adfe-a3355dbf5b44)
 Call ID: 9ff2973e-3061-4d21-adfe-a3355dbf5b44
  Args:
    type: :Person
    source: Crown_Princess_Margareta_of_Romania
  AddTriple (75a641e5-f45f-4bb5-b3be-b586ad6633ca)
 Call ID: 75a641e5-f45f-4bb5-b3be-b586ad6633ca
  Args:
    source: Crown_Princess_Margareta_of_Romania
    target: Princess_Elena_of_Romania
    relation: :isSisterOf
  AddTriple (72599f2b-dbeb-487a-8a4d-e10e3356b7d5)
 Call ID: 72599f2b-dbeb-487a-8a4d-e10e3356b7d5
  Args:
    source: Crown_Princess_Margareta_of_Romania
    target: Queen_Anne_of_Romania
    relation: :hasMother
  AddTriple (dc8188eb-92ca-4aec-97c1-ec0bfa141732)
 Call ID: dc8188eb-92ca-4aec-97c1-ec0bfa141732
  Args:
    source: Crown_Princess_Margareta_of_Romania
    target: King_Michael_I_of_Romania
    relation: :hasFather
  AssignClass (cdbc4869-05f2-473e-b9cb-4e8dde159a04)
 Call ID: cdbc4869-05f2-473e-b9cb-4e8dde159a04
  Args:
    type: :Woman
    source: Alina-Maria_Binder
  AssignClass (65247709-1218-476d-ac86-45609fa79a28)
 Call ID: 65247709-1218-476d-ac86-45609fa79a28
  Args:
    type: :Person
    source: Alina-Maria_Binder
  AddLiteral (6061f3a4-da16-4920-ae40-f7879d85bea4)
 Call ID: 6061f3a4-da16-4920-ae40-f7879d85bea4
  Args:
    literal_value: 2017
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
  AddTriple (f5c3d602-3063-4989-a639-b30599d07682)
 Call ID: f5c3d602-3063-4989-a639-b30599d07682
  Args:
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    target: Alina-Maria_Binder
    relation: :hasRelation
  AssignClass (21b26eb6-3725-4448-b04d-60dbc4a80b24)
 Call ID: 21b26eb6-3725-4448-b04d-60dbc4a80b24
  Args:
    type: :Man
    source: Alexander_Nixon
  AssignClass (aeac7410-ae27-488f-bdce-08a01a9ee737)
 Call ID: aeac7410-ae27-488f-bdce-08a01a9ee737
  Args:
    type: :Person
    source: Alexander_Nixon
  AssignClass (9fe963c4-b688-4bef-8228-9b5c872dae32)
 Call ID: 9fe963c4-b688-4bef-8228-9b5c872dae32
  Args:
    type: :Man
    source: Radu_Duda
  AssignClass (ea4d8868-09f5-4079-9f08-fcb08d247b6e)
 Call ID: ea4d8868-09f5-4079-9f08-fcb08d247b6e
  Args:
    source: Radu_Duda
    type: :Person
  AssignClass (24099f32-abed-4769-8d3c-3c94e36b9806)
 Call ID: 24099f32-abed-4769-8d3c-3c94e36b9806
  Args:
    source: Nicoleta_Cîrjan
    type: :Woman
  AssignClass (a9f4dc78-508e-4491-bb76-cf6ff9446315)
 Call ID: a9f4dc78-508e-4491-bb76-cf6ff9446315
  Args:
    type: :Person
    source: Nicoleta_Cîrjan
  AssignClass (dab1b97c-4345-44bc-98bf-c8f49df7a80f)
 Call ID: dab1b97c-4345-44bc-98bf-c8f49df7a80f
  Args:
    type: :Woman
    source: Illegitimate_Daughter_of_Nicholas
  AssignClass (f197e175-6012-405d-a55f-c91c883fb083)
 Call ID: f197e175-6012-405d-a55f-c91c883fb083
  Args:
    type: :Person
    source: Illegitimate_Daughter_of_Nicholas
  AddTriple (d0da03fa-8a4a-4b47-9435-06effaf82e75)
 Call ID: d0da03fa-8a4a-4b47-9435-06effaf82e75
  Args:
    source: Illegitimate_Daughter_of_Nicholas
    relation: :hasFather
    target: Nicholas_Michael_de_Roumanie_Medforth-Mills
  AddTriple (d0637b9b-b553-47fc-9166-94f47c829038)
 Call ID: d0637b9b-b553-47fc-9166-94f47c829038
  Args:
    source: Illegitimate_Daughter_of_Nicholas
    relation: :hasMother
    target: Nicoleta_Cîrjan
  Finish (388b3c26-2b99-4faa-b0e9-3edec5bec9dc)
 Call ID: 388b3c26-2b99-4faa-b0e9-3edec5bec9dc
  Args: