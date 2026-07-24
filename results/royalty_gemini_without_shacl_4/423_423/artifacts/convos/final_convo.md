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
Prince Wilhelm Victor of Prussia (German: Wilhelm Viktor Ernst Freund Friedrich Georg Adalbert; 15 February 1919 – 7 February 1989) was a German royal, soldier and diplomat.
Life

Prince Wilhelm Victor was a grandson of Emperor Wilhelm II and the youngest child of Prince Adalbert of Prussia (1884–1948) and Princess Adelheid "Adi" of Saxe-Meiningen (1891–1971).
His father, Prince Adalbert carried also the title "Graf von Lingen".
His only surviving sister, Princess Viktoria Marina (1917–1981) married Kirby William Patterson (1907–1984).
Marriage

Prince Wilhelm Victor married at Donaueschingen 20 July 1944 Marie Antoinette, Countess of Hoyos-Stichsenstein (Hohenthurm, 27 June 1920 – Marbella 1 March 2004),  daughter of Friedrich, Count of Hoyos-Stichsenstein (1876–1951) and Countess Wilhelmine von Wuthenau-Hohenthurm (1895–1983), niece of Sophie, Duchess of Hohenberg.
They had the following issue:


Death

Prince Wilhelm Viktor died on 7 February 1989 at age 69.



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
  AssignClass (8c44c60f-3d1f-4a1c-81af-c105a2cd61c9)
 Call ID: 8c44c60f-3d1f-4a1c-81af-c105a2cd61c9
  Args:
    type: :Man
    source: :Prince_Wilhelm_Victor_of_Prussia
  AssignClass (9e350e5e-ad02-444d-b81e-759245188277)
 Call ID: 9e350e5e-ad02-444d-b81e-759245188277
  Args:
    type: :Person
    source: :Prince_Wilhelm_Victor_of_Prussia
  AddLiteral (f946060b-db35-4703-9b54-0203a5f1b604)
 Call ID: f946060b-db35-4703-9b54-0203a5f1b604
  Args:
    literal_type: xsd:integer
    literal_value: 1919
    source: :Prince_Wilhelm_Victor_of_Prussia
    relation: :hasBirthYear
  AddLiteral (8f1de270-d5f1-4fff-8a6d-065ff29673db)
 Call ID: 8f1de270-d5f1-4fff-8a6d-065ff29673db
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Prince_Wilhelm_Victor_of_Prussia
    literal_value: 1989
  AssignClass (9327f06b-d2a9-4610-a620-d38fb8e7c47e)
 Call ID: 9327f06b-d2a9-4610-a620-d38fb8e7c47e
  Args:
    type: :Man
    source: :Emperor_Wilhelm_II
  AssignClass (ed1cc266-cad4-4d25-bd60-856d5934a00f)
 Call ID: ed1cc266-cad4-4d25-bd60-856d5934a00f
  Args:
    type: :Person
    source: :Emperor_Wilhelm_II
  AddTriple (6640d3e0-7688-45c9-86fc-d3a1d447e1a6)
 Call ID: 6640d3e0-7688-45c9-86fc-d3a1d447e1a6
  Args:
    relation: :isAncestorOf
    source: :Emperor_Wilhelm_II
    target: :Prince_Wilhelm_Victor_of_Prussia
  AssignClass (9dd7a00e-09e4-4781-aab2-e5d56d1e03b2)
 Call ID: 9dd7a00e-09e4-4781-aab2-e5d56d1e03b2
  Args:
    type: :Man
    source: :Prince_Adalbert_of_Prussia
  AssignClass (8f56e0aa-86b7-4315-81c8-f02446a68c0f)
 Call ID: 8f56e0aa-86b7-4315-81c8-f02446a68c0f
  Args:
    type: :Person
    source: :Prince_Adalbert_of_Prussia
  AddLiteral (7b547372-25be-48c3-919a-f2df30488ee2)
 Call ID: 7b547372-25be-48c3-919a-f2df30488ee2
  Args:
    literal_value: 1884
    relation: :hasBirthYear
    source: :Prince_Adalbert_of_Prussia
    literal_type: xsd:integer
  AddLiteral (706639ae-1083-41a1-b7e9-584ce52bea86)
 Call ID: 706639ae-1083-41a1-b7e9-584ce52bea86
  Args:
    literal_type: xsd:integer
    literal_value: 1948
    source: :Prince_Adalbert_of_Prussia
    relation: :hasDeathYear
  AddLiteral (92bed93b-ac56-413b-b1d8-c583ddbba6e5)
 Call ID: 92bed93b-ac56-413b-b1d8-c583ddbba6e5
  Args:
    relation: :alsoKnownAs
    source: :Prince_Adalbert_of_Prussia
    literal_value: Graf von Lingen
    literal_type: xsd:string
  AssignClass (46997b0d-e9e6-4d48-863d-f4ed29bfea77)
 Call ID: 46997b0d-e9e6-4d48-863d-f4ed29bfea77
  Args:
    type: :Woman
    source: :Princess_Adelheid_of_Saxe-Meiningen
  AssignClass (83207aad-b33f-4729-bdad-44e1ca36caef)
 Call ID: 83207aad-b33f-4729-bdad-44e1ca36caef
  Args:
    type: :Person
    source: :Princess_Adelheid_of_Saxe-Meiningen
  AddLiteral (381da59b-7ab6-4088-a8bf-ee4299b4f6bb)
 Call ID: 381da59b-7ab6-4088-a8bf-ee4299b4f6bb
  Args:
    source: :Princess_Adelheid_of_Saxe-Meiningen
    relation: :hasBirthYear
    literal_value: 1891
    literal_type: xsd:integer
  AddLiteral (8a464403-198c-4729-927f-fba4b3696419)
 Call ID: 8a464403-198c-4729-927f-fba4b3696419
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: :Princess_Adelheid_of_Saxe-Meiningen
    literal_value: 1971
  AddTriple (225c55b1-55f0-407b-b62e-dae7c846a2dc)
 Call ID: 225c55b1-55f0-407b-b62e-dae7c846a2dc
  Args:
    target: :Prince_Adalbert_of_Prussia
    source: :Prince_Wilhelm_Victor_of_Prussia
    relation: :hasFather
  AddTriple (e427f80a-f54c-4d40-a7ae-46dfb90b58c3)
 Call ID: e427f80a-f54c-4d40-a7ae-46dfb90b58c3
  Args:
    target: :Princess_Adelheid_of_Saxe-Meiningen
    source: :Prince_Wilhelm_Victor_of_Prussia
    relation: :hasMother
  AssignClass (994d057a-525e-45c1-aae7-e22c7b31ceb1)
 Call ID: 994d057a-525e-45c1-aae7-e22c7b31ceb1
  Args:
    type: :Woman
    source: :Princess_Viktoria_Marina
  AssignClass (ce7f6426-06e9-4315-8695-4d2eb5eb0bf5)
 Call ID: ce7f6426-06e9-4315-8695-4d2eb5eb0bf5
  Args:
    type: :Person
    source: :Princess_Viktoria_Marina
  AddLiteral (d9edb130-e004-4e6c-8897-7850000548d2)
 Call ID: d9edb130-e004-4e6c-8897-7850000548d2
  Args:
    literal_value: 1917
    source: :Princess_Viktoria_Marina
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (d0a271b6-3903-4440-8585-f5d5ee11241d)
 Call ID: d0a271b6-3903-4440-8585-f5d5ee11241d
  Args:
    literal_value: 1981
    relation: :hasDeathYear
    source: :Princess_Viktoria_Marina
    literal_type: xsd:integer
  AddTriple (c9a77bae-963c-4976-986a-8b8651dde5a0)
 Call ID: c9a77bae-963c-4976-986a-8b8651dde5a0
  Args:
    source: :Princess_Viktoria_Marina
    relation: :isSisterOf
    target: :Prince_Wilhelm_Victor_of_Prussia
  AssignClass (ce178726-1b67-45cc-9074-073f90ddee28)
 Call ID: ce178726-1b67-45cc-9074-073f90ddee28
  Args:
    type: :Man
    source: :Kirby_William_Patterson
  AssignClass (c8f6abd0-54d7-4926-ac01-20e195c7a644)
 Call ID: c8f6abd0-54d7-4926-ac01-20e195c7a644
  Args:
    type: :Person
    source: :Kirby_William_Patterson
  AddLiteral (fead8f86-f9e5-4561-ae51-55d182329978)
 Call ID: fead8f86-f9e5-4561-ae51-55d182329978
  Args:
    source: :Kirby_William_Patterson
    relation: :hasBirthYear
    literal_value: 1907
    literal_type: xsd:integer
  AddLiteral (1b001d56-8b2e-44cc-b12a-62d2c1e832bd)
 Call ID: 1b001d56-8b2e-44cc-b12a-62d2c1e832bd
  Args:
    literal_type: xsd:integer
    literal_value: 1984
    source: :Kirby_William_Patterson
    relation: :hasDeathYear
  AddTriple (85be360e-86bd-41a3-b99f-4649b367603d)
 Call ID: 85be360e-86bd-41a3-b99f-4649b367603d
  Args:
    source: :Princess_Viktoria_Marina
    relation: :hasRelation
    target: :Kirby_William_Patterson
  AssignClass (afbbf0ac-7310-444c-8c41-bc780d548e54)
 Call ID: afbbf0ac-7310-444c-8c41-bc780d548e54
  Args:
    type: :Woman
    source: :Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
  AssignClass (f276b409-3c7d-4e61-8446-96915e20a8f7)
 Call ID: f276b409-3c7d-4e61-8446-96915e20a8f7
  Args:
    type: :Person
    source: :Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
  AddLiteral (d7f7c8f0-5a11-48c7-b0ca-242c6603a38c)
 Call ID: d7f7c8f0-5a11-48c7-b0ca-242c6603a38c
  Args:
    literal_value: 1920
    relation: :hasBirthYear
    source: :Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    literal_type: xsd:integer
  AddLiteral (16ffdafb-3602-4207-8963-9f5a427f0850)
 Call ID: 16ffdafb-3602-4207-8963-9f5a427f0850
  Args:
    literal_type: xsd:integer
    literal_value: 2004
    source: :Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    relation: :hasDeathYear
  AddLiteral (58a2cc5e-ec51-445a-a75e-58ca543882ad)
 Call ID: 58a2cc5e-ec51-445a-a75e-58ca543882ad
  Args:
    literal_type: xsd:integer
    source: :Prince_Wilhelm_Victor_of_Prussia
    relation: :hasMarriageYear
    literal_value: 1944
  AddTriple (7ed48974-ba38-45b5-947a-aed68c524bbb)
 Call ID: 7ed48974-ba38-45b5-947a-aed68c524bbb
  Args:
    relation: :hasRelation
    source: :Prince_Wilhelm_Victor_of_Prussia
    target: :Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
  AssignClass (ebac064d-456b-4dc7-8b76-4ac170835628)
 Call ID: ebac064d-456b-4dc7-8b76-4ac170835628
  Args:
    type: :Man
    source: :Friedrich_Count_of_Hoyos-Stichsenstein
  AssignClass (0350622b-6d89-4f22-9a0c-8b56ccc194b4)
 Call ID: 0350622b-6d89-4f22-9a0c-8b56ccc194b4
  Args:
    type: :Person
    source: :Friedrich_Count_of_Hoyos-Stichsenstein
  AddLiteral (b9c5a8d5-4e54-41ca-89c3-9fba9e49655a)
 Call ID: b9c5a8d5-4e54-41ca-89c3-9fba9e49655a
  Args:
    literal_type: xsd:integer
    source: :Friedrich_Count_of_Hoyos-Stichsenstein
    relation: :hasBirthYear
    literal_value: 1876
  AddLiteral (661b88ea-a347-4c17-939c-c1a156db8a9d)
 Call ID: 661b88ea-a347-4c17-939c-c1a156db8a9d
  Args:
    relation: :hasDeathYear
    source: :Friedrich_Count_of_Hoyos-Stichsenstein
    literal_value: 1951
    literal_type: xsd:integer
  AssignClass (f874b039-8e6d-4c2a-ae88-baa311c76d18)
 Call ID: f874b039-8e6d-4c2a-ae88-baa311c76d18
  Args:
    type: :Woman
    source: :Countess_Wilhelmine_von_Wuthenau-Hohenthurm
  AssignClass (b7f5bc5d-07ea-4658-81f3-3d8c6b86ebb5)
 Call ID: b7f5bc5d-07ea-4658-81f3-3d8c6b86ebb5
  Args:
    type: :Person
    source: :Countess_Wilhelmine_von_Wuthenau-Hohenthurm
  AddLiteral (7ac33031-3359-4c32-9976-4492e1b19dfd)
 Call ID: 7ac33031-3359-4c32-9976-4492e1b19dfd
  Args:
    literal_type: xsd:integer
    literal_value: 1895
    source: :Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    relation: :hasBirthYear
  AddLiteral (f713a49f-1a9c-4d59-a285-a68d5f478ddc)
 Call ID: f713a49f-1a9c-4d59-a285-a68d5f478ddc
  Args:
    literal_type: xsd:integer
    literal_value: 1983
    relation: :hasDeathYear
    source: :Countess_Wilhelmine_von_Wuthenau-Hohenthurm
  AddTriple (cce6ebc0-91ad-4c80-8eac-eb7070ee54e5)
 Call ID: cce6ebc0-91ad-4c80-8eac-eb7070ee54e5
  Args:
    target: :Friedrich_Count_of_Hoyos-Stichsenstein
    source: :Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    relation: :hasFather
  AddTriple (e38f5c0a-5427-4c5f-a3ea-ec1d2bdc816b)
 Call ID: e38f5c0a-5427-4c5f-a3ea-ec1d2bdc816b
  Args:
    target: :Countess_Wilhelmine_von_Wuthenau-Hohenthurm
    source: :Marie_Antoinette_Countess_of_Hoyos-Stichsenstein
    relation: :hasMother
  AssignClass (1c61126d-1600-47e4-bee0-66667667cbdb)
 Call ID: 1c61126d-1600-47e4-bee0-66667667cbdb
  Args:
    type: :Woman
    source: :Sophie_Duchess_of_Hohenberg
  AssignClass (54d7555e-ef60-4f4f-b2a3-5213f4c819dc)
 Call ID: 54d7555e-ef60-4f4f-b2a3-5213f4c819dc
  Args:
    type: :Person
    source: :Sophie_Duchess_of_Hohenberg
  Finish (7f43964c-a14c-44d2-b9ee-01b7db835fe6)
 Call ID: 7f43964c-a14c-44d2-b9ee-01b7db835fe6
  Args: