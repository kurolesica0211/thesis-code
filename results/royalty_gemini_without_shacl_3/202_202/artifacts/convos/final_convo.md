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
Archduke Gottfried of Austria (German: Gottfried Maria Joseph Peter Ferdinand Hubert Anton Rupert Leopold Heinrich Ignaz Alfons, Erzherzog von Österreich, Prinz von Toskana; 14 March 1902 – 21 January 1984), also styled as Gottfried Erzherzog von Österreich, was an Archduke of Austria and claimant to the defunct throne of the Grand Duchy of Tuscany.
Biography

On 20 December 1866, Goffredo's grandfather, Ferdinando IV, the last Grand Duke of Tuscany, and his children were readmitted to the imperial family.
The House of Tuscany ceased to exist as a sovereign branch and merged with the Austrian imperial house.
Ferdinand was able to maintain his fons honorum vita natural durante, while his children became only imperial princes (archdukes of Austria) and no longer princes/princesses of Tuscany.
The Grand Magistry of the Order of St Stephen died out with the death of Ferdinand IV.
In fact, after the death of Grand Duke Ferdinand IV in 1908, Emperor Franz Joseph I forbade the acceptance of the title of Grand Duke or Prince or Princess of Tuscany: none of Ferdinand IV's children born after 1866 accepted the title of Prince or Grand Duke of Tuscany.
They were also unable to legitimately take possession of the extinct dynastic orders, previously conferred by the Grand Dukes of Tuscany.
While his grandfather had kept the title of Grand Duke of Tuscany after the abolition of the dukedom in 1860, he had abdicated it in favor of the Austrian Emperor in 1870.
Peter Ferdinand, Goffredo's father, never  claimed the title of Grand Duke of Tuscany.
The former Prime Minister of Saxony and later Imperial and Household Minister Beust declared: "The Tuscan Grand Ducal family has lost its sovereign rights as a result of political events.
The Grand Dukes Leopold and Ferdinand and their more famous brothers are therefore from now on to be considered only as Archdukes of Austria and to be treated in accordance with the Statute of the High Noble Family of 3 February 1839.
"


Family

Gottfried was born in Linz, Austria-Hungary, the eldest child and son  of Archduke Peter Ferdinand of Austria and his wife Princess Maria Cristina of Bourbon-Two Sicilies.
Gottfried was raised with his three siblings in Salzburg and Vienna until the end of World War I in 1918, when his family emigrated to Lucerne, Switzerland.
Marriage and issue

Gottfried married Princess Dorothea of Bavaria, fifth child and fourth daughter of Prince Franz of Bavaria and his wife Princess Isabella Antonie of Croÿ, on 2 August 1938 civilly and religiously on 3 August 1938 in Sárvár, Kingdom of Hungary.
Around 1970, in violation of the decree of Emperor Franz Joseph I of 1866 and ignoring the abdication of his grandfather last Grand Duke of Tuscany Ferdinand IV signed in Lindau on Lake Constance in 1870, he assumed the title of Grand Duke of Tuscany without the permission of the head of the imperial and royal house.
Gottfried and Dorothea had issue:


Honours

Ancestry

References



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
  AssignClass (f0dbfff2-1484-4c6e-906d-1616dadd65a8)
 Call ID: f0dbfff2-1484-4c6e-906d-1616dadd65a8
  Args:
    type: :Man
    source: Gottfried
  AssignClass (833ff5e0-fa4a-4b32-8daa-c952a570d920)
 Call ID: 833ff5e0-fa4a-4b32-8daa-c952a570d920
  Args:
    type: :Person
    source: Gottfried
  AddLiteral (b4969e17-f51e-4bb0-a194-216bba76c5c5)
 Call ID: b4969e17-f51e-4bb0-a194-216bba76c5c5
  Args:
    relation: :hasBirthYear
    literal_value: 1902
    literal_type: xsd:integer
    source: Gottfried
  AddLiteral (803953d4-5691-467d-8bcf-00263bb71575)
 Call ID: 803953d4-5691-467d-8bcf-00263bb71575
  Args:
    literal_value: 1984
    relation: :hasDeathYear
    source: Gottfried
    literal_type: xsd:integer
  AssignClass (4a852046-8169-4386-9b5c-15010b12d193)
 Call ID: 4a852046-8169-4386-9b5c-15010b12d193
  Args:
    type: :Man
    source: Ferdinand_IV
  AssignClass (585c1712-5928-41d2-af9a-12614cc5720d)
 Call ID: 585c1712-5928-41d2-af9a-12614cc5720d
  Args:
    type: :Person
    source: Ferdinand_IV
  AssignClass (603ab54e-26d6-40d9-88d4-39f978afe635)
 Call ID: 603ab54e-26d6-40d9-88d4-39f978afe635
  Args:
    type: :Man
    source: Peter_Ferdinand
  AssignClass (98c5d14a-855d-4218-bf3f-01d5ad26eb7d)
 Call ID: 98c5d14a-855d-4218-bf3f-01d5ad26eb7d
  Args:
    type: :Person
    source: Peter_Ferdinand
  AssignClass (e2dadcf8-15dc-4a47-be16-40c9f4a1e2fb)
 Call ID: e2dadcf8-15dc-4a47-be16-40c9f4a1e2fb
  Args:
    type: :Woman
    source: Maria_Cristina
  AssignClass (f8450bd0-ce94-4cb1-ba2d-c8a6ac249f63)
 Call ID: f8450bd0-ce94-4cb1-ba2d-c8a6ac249f63
  Args:
    type: :Person
    source: Maria_Cristina
  AddTriple (3632ed15-e9cb-495c-aaa1-505c8bd32f6e)
 Call ID: 3632ed15-e9cb-495c-aaa1-505c8bd32f6e
  Args:
    source: Ferdinand_IV
    target: Peter_Ferdinand
    relation: :isFatherOf
  AddTriple (2d78eb68-d4fc-42a4-9f1e-17381909fbcf)
 Call ID: 2d78eb68-d4fc-42a4-9f1e-17381909fbcf
  Args:
    relation: :isFatherOf
    source: Peter_Ferdinand
    target: Gottfried
  AddTriple (3dfe200a-8390-4a1d-b09d-8a09c118a2a5)
 Call ID: 3dfe200a-8390-4a1d-b09d-8a09c118a2a5
  Args:
    relation: :isMotherOf
    target: Gottfried
    source: Maria_Cristina
  AssignClass (687b26d9-0b65-46f3-9176-3ef27688d7d0)
 Call ID: 687b26d9-0b65-46f3-9176-3ef27688d7d0
  Args:
    type: :Woman
    source: Dorothea_of_Bavaria
  AssignClass (3c955fb0-1555-4675-8f50-d507dc052f36)
 Call ID: 3c955fb0-1555-4675-8f50-d507dc052f36
  Args:
    type: :Person
    source: Dorothea_of_Bavaria
  AddTriple (5528a571-e63e-4f76-a2cf-c4f2dbcbe11d)
 Call ID: 5528a571-e63e-4f76-a2cf-c4f2dbcbe11d
  Args:
    source: Gottfried
    target: Dorothea_of_Bavaria
    relation: :hasRelation
  AddLiteral (e5f5837c-b8e9-4e6c-940d-f83547ee082a)
 Call ID: e5f5837c-b8e9-4e6c-940d-f83547ee082a
  Args:
    literal_type: xsd:integer
    source: Gottfried
    relation: :hasMarriageYear
    literal_value: 1938
  AssignClass (feb5591a-910e-4f80-8ae6-0597a118f72f)
 Call ID: feb5591a-910e-4f80-8ae6-0597a118f72f
  Args:
    type: :Man
    source: Franz_of_Bavaria
  AssignClass (3c8f8216-2520-4694-9b54-ba96f7d71c6b)
 Call ID: 3c8f8216-2520-4694-9b54-ba96f7d71c6b
  Args:
    type: :Person
    source: Franz_of_Bavaria
  AssignClass (1228a7ca-94b5-43db-a224-066b20c3c134)
 Call ID: 1228a7ca-94b5-43db-a224-066b20c3c134
  Args:
    type: :Woman
    source: Isabella_Antonie_of_Croy
  AssignClass (972ac004-6668-4d17-9f38-6a0f4fe0d923)
 Call ID: 972ac004-6668-4d17-9f38-6a0f4fe0d923
  Args:
    type: :Person
    source: Isabella_Antonie_of_Croy
  AddTriple (e979a3f0-33d1-4d6f-8205-8815555a6fde)
 Call ID: e979a3f0-33d1-4d6f-8205-8815555a6fde
  Args:
    source: Franz_of_Bavaria
    target: Dorothea_of_Bavaria
    relation: :isFatherOf
  AddTriple (77db0ee2-5d6e-4ca6-a3c0-5d18d290ab01)
 Call ID: 77db0ee2-5d6e-4ca6-a3c0-5d18d290ab01
  Args:
    target: Dorothea_of_Bavaria
    source: Isabella_Antonie_of_Croy
    relation: :isMotherOf
  Finish (d6dc82fc-3c37-4bf2-a4f6-d946c33d0b7d)
 Call ID: d6dc82fc-3c37-4bf2-a4f6-d946c33d0b7d
  Args: