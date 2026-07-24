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
Franz Ulrich, 11th Prince Kinsky of Wchinitz and Tettau (German: Franz Ulrich Johannes Clemens Christophorus Antonius Bonaventura Maria Fürst Kinsky von Wchinitz und Tettau; 7 October 1936 – 2 April 2009) was the titular Prince Kinsky of Wchinitz and Tettau as well the head of an ancient House of Kinsky.
Early life

Franz Ulrich was born at Vienna, Federal State of Austria, as the youngest son of Ulrich, 10th Prince Kinsky of Wchinitz and Tettau by his second marriage to Baroness Marie Julia Mathilde von dem Bussche-Haddenhausen (1900–1974), the eldest daughter of Baron Hilmar von dem Bussche-Haddenhausen.
Franz Ulrich became the titular Prince upon the death of his father in 1938.
He was first cousin of Countess Marie Aglaë Kinsky of Wchinitz and Tettau who later became Princess consort of Liechtenstein, and second cousin of Claus von Amsberg, Prince consort of Queen Beatrix of the Netherlands, both descendants of Baron Julius von dem Bussche-Haddenhausen.
In 1942, Franz Ulrich inherited several estates from the Kinsky family, including the Kinsky Palace in Old Town Square in Prague.
Starting in 2003, Franz Ulrich complained against various Czech courts for the return of the assets.
Marriage and family

Franz Ulrich married on 14 April 1965 in Buenos Aires to Roberta Cavanagh (1942–2002), daughter of Roberto Cavanagh and his wife, Anne Rowell.
After Kinsky's death, his son and his widow, Countess Helena Victoria Hutten-Czapska entered a legal dispute over Kinsky's properties.
Later life

The Prince died on 2 April 2009, aged 72.



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
  AssignClass (1f44d0d6-f85e-48da-83ef-38d0a95974d9)
 Call ID: 1f44d0d6-f85e-48da-83ef-38d0a95974d9
  Args:
    source: FranzUlrich
    type: :Man
  AssignClass (150ee0eb-c0e6-4723-beb4-57c2eeb93771)
 Call ID: 150ee0eb-c0e6-4723-beb4-57c2eeb93771
  Args:
    type: :Person
    source: FranzUlrich
  AddLiteral (f5ef51f1-888e-4d01-8133-accdf65e0266)
 Call ID: f5ef51f1-888e-4d01-8133-accdf65e0266
  Args:
    literal_value: 1936
    relation: :hasBirthYear
    source: FranzUlrich
    literal_type: xsd:integer
  AddLiteral (e329f73b-fbf7-4c8d-a408-7491ea2dae26)
 Call ID: e329f73b-fbf7-4c8d-a408-7491ea2dae26
  Args:
    source: FranzUlrich
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2009
  AssignClass (b7d36fdc-b9dd-4583-a441-202c43a78e12)
 Call ID: b7d36fdc-b9dd-4583-a441-202c43a78e12
  Args:
    type: :Man
    source: Ulrich10thPrinceKinsky
  AssignClass (ebeb1ca3-800f-47b8-8d73-628c09af3775)
 Call ID: ebeb1ca3-800f-47b8-8d73-628c09af3775
  Args:
    source: Ulrich10thPrinceKinsky
    type: :Ancestor
  AddTriple (da9f6915-a0ec-4978-bdd7-d90661bf8bc1)
 Call ID: da9f6915-a0ec-4978-bdd7-d90661bf8bc1
  Args:
    target: Ulrich10thPrinceKinsky
    source: FranzUlrich
    relation: :hasFather
  AssignClass (6bf29b07-5e48-4b79-87db-d4b7d2c47e61)
 Call ID: 6bf29b07-5e48-4b79-87db-d4b7d2c47e61
  Args:
    source: MarieJuliaMathildeVondemBusscheHaddenhausen
    type: :Woman
  AssignClass (32cefe4c-41a8-4c86-8ea8-d705c8c24909)
 Call ID: 32cefe4c-41a8-4c86-8ea8-d705c8c24909
  Args:
    source: MarieJuliaMathildeVondemBusscheHaddenhausen
    type: :Ancestor
  AddLiteral (6a321b66-cc57-4be1-8ac5-a8c99989e3e8)
 Call ID: 6a321b66-cc57-4be1-8ac5-a8c99989e3e8
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: MarieJuliaMathildeVondemBusscheHaddenhausen
    literal_value: 1900
  AddLiteral (8db3b464-6c75-4ce9-8aac-88f940f169df)
 Call ID: 8db3b464-6c75-4ce9-8aac-88f940f169df
  Args:
    literal_value: 1974
    source: MarieJuliaMathildeVondemBusscheHaddenhausen
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (9bdec1f1-c076-499e-b19e-bc666d646849)
 Call ID: 9bdec1f1-c076-499e-b19e-bc666d646849
  Args:
    relation: :hasMother
    source: FranzUlrich
    target: MarieJuliaMathildeVondemBusscheHaddenhausen
  AssignClass (d15d6b2c-dd6c-4389-a94a-d7fb14d6f405)
 Call ID: d15d6b2c-dd6c-4389-a94a-d7fb14d6f405
  Args:
    type: :Man
    source: HilmarVondemBusscheHaddenhausen
  AssignClass (5f781b7c-e974-448f-a3d7-18580b5bd608)
 Call ID: 5f781b7c-e974-448f-a3d7-18580b5bd608
  Args:
    type: :Ancestor
    source: HilmarVondemBusscheHaddenhausen
  AddTriple (ffa8a8b2-14c4-4794-9b81-3e896f70a95b)
 Call ID: ffa8a8b2-14c4-4794-9b81-3e896f70a95b
  Args:
    source: MarieJuliaMathildeVondemBusscheHaddenhausen
    target: HilmarVondemBusscheHaddenhausen
    relation: :hasFather
  AssignClass (7e8ba193-9b83-468c-b73c-5f8129ae00f7)
 Call ID: 7e8ba193-9b83-468c-b73c-5f8129ae00f7
  Args:
    type: :Woman
    source: RobertaCavanagh
  AssignClass (b2cb221e-488e-4b59-b490-bf9ba98b19bb)
 Call ID: b2cb221e-488e-4b59-b490-bf9ba98b19bb
  Args:
    type: :Person
    source: RobertaCavanagh
  AddLiteral (99c61438-d257-4ec8-8fca-2e4a93219c6b)
 Call ID: 99c61438-d257-4ec8-8fca-2e4a93219c6b
  Args:
    literal_value: 1942
    relation: :hasBirthYear
    source: RobertaCavanagh
    literal_type: xsd:integer
  AddLiteral (50446cb8-4f8a-4f8c-9de7-ddf1bb0f0fcc)
 Call ID: 50446cb8-4f8a-4f8c-9de7-ddf1bb0f0fcc
  Args:
    literal_value: 2002
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: RobertaCavanagh
  AddTriple (a16c3197-45a2-421d-b2ea-f19c7d760e40)
 Call ID: a16c3197-45a2-421d-b2ea-f19c7d760e40
  Args:
    target: RobertaCavanagh
    source: FranzUlrich
    relation: :hasRelation
  AddLiteral (e379aff5-07fb-4a53-b807-193a9a14e9b7)
 Call ID: e379aff5-07fb-4a53-b807-193a9a14e9b7
  Args:
    literal_value: 1965
    literal_type: xsd:integer
    source: FranzUlrich
    relation: :hasMarriageYear
  AssignClass (bb210361-82d4-4307-817e-ca9556012980)
 Call ID: bb210361-82d4-4307-817e-ca9556012980
  Args:
    type: :Man
    source: RobertoCavanagh
  AssignClass (1f976d59-196f-4775-a2f6-95bf09681c3e)
 Call ID: 1f976d59-196f-4775-a2f6-95bf09681c3e
  Args:
    type: :Person
    source: RobertoCavanagh
  AddTriple (ad52e88a-6f20-4dc4-b465-d82c46263886)
 Call ID: ad52e88a-6f20-4dc4-b465-d82c46263886
  Args:
    relation: :hasFather
    target: RobertoCavanagh
    source: RobertaCavanagh
  AssignClass (2ab36cc7-f4a7-4ecd-9f8d-639a6642914e)
 Call ID: 2ab36cc7-f4a7-4ecd-9f8d-639a6642914e
  Args:
    source: AnneRowell
    type: :Woman
  AssignClass (40b2af10-42e3-4b52-b375-7665eb001dac)
 Call ID: 40b2af10-42e3-4b52-b375-7665eb001dac
  Args:
    source: AnneRowell
    type: :Person
  AddTriple (56b249a6-490a-492b-b522-13e97fad2beb)
 Call ID: 56b249a6-490a-492b-b522-13e97fad2beb
  Args:
    source: RobertaCavanagh
    target: AnneRowell
    relation: :hasMother
  AssignClass (27ac15e5-c8b7-4009-80a2-3fac29e4cc6d)
 Call ID: 27ac15e5-c8b7-4009-80a2-3fac29e4cc6d
  Args:
    source: HelenaVictoriaHuttenCzapska
    type: :Woman
  AssignClass (35b869eb-6084-44fe-acaf-b30ad1d05d14)
 Call ID: 35b869eb-6084-44fe-acaf-b30ad1d05d14
  Args:
    type: :Person
    source: HelenaVictoriaHuttenCzapska
  AssignClass (17de8aa3-b31a-4d37-991d-bb809328cea6)
 Call ID: 17de8aa3-b31a-4d37-991d-bb809328cea6
  Args:
    source: KinskySon
    type: :Man
  AssignClass (75365135-2087-4523-8f72-94eb70cefb1e)
 Call ID: 75365135-2087-4523-8f72-94eb70cefb1e
  Args:
    type: :Person
    source: KinskySon
  AddTriple (dbe43a11-f4e0-4f2b-bd11-db27c48dc1d2)
 Call ID: dbe43a11-f4e0-4f2b-bd11-db27c48dc1d2
  Args:
    relation: :hasFather
    source: KinskySon
    target: FranzUlrich
  Finish (ec334462-8afe-4ce8-a5a2-9d351d77d7ee)
 Call ID: ec334462-8afe-4ce8-a5a2-9d351d77d7ee
  Args: