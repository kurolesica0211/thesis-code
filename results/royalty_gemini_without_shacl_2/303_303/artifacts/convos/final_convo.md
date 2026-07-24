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
Prince Tomislav of Yugoslavia (Serbian: Томислав Карађорђевић, Tomislav Karađorđević; 19 January 1928 – 12 July 2000) was a member of the House of Karađorđević, the second son of King Alexander I and Queen Maria of Yugoslavia.
He was a younger brother of King Peter II of Yugoslavia and a former nephew-in-law to Queen Elizabeth II and Prince Philip.
Early life and education

Prince Tomislav was born on 19 January 1928, on Epiphany according to the Julian calendar used by the Serbian Orthodox Church, at 1 am, as the second son of the sovereign of the then Kingdom of Serbs, Croats and Slovenes (later the Kingdom of Yugoslavia), Alexander I and Queen Maria, the second daughter of King Ferdinand of Romania and his wife Queen Marie.
He was baptized on 25 January in a salon of the New Palace in Belgrade, with the British Minister to the Yugoslav Court, Kennard, representing the godfather King George V, with water from the Vardar and Danube rivers and the Adriatic Sea.
The Prince was named after Tomislav of Croatia, the King of medieval Croatia.
At the beginning of February 1928, a delegation was sent from Županjac (present-day Tomislavgrad) headed by the parish priest Šimun Ančić who handed Alexander the resolution in which the population of the Srez of Županjac asks him to change the name of the srez to Tomislavgrad, in honour of his son and Tomislav of Croatia.
Not long after, Alexander granted them their petition but dropped Tomislav of Croatia from his decree.
He began his elementary education at the Belgrade Palace but in 1937 he started to attend Sandroyd School in Cobham, Surrey, and then, following the school's relocation, in Tollard Royal, Wiltshire.
Events in Yugoslavia

In 1934 when he was only six, Prince Tomislav's father, Alexander I, was assassinated and his elder brother Peter succeeded to the throne as King Peter II of Yugoslavia.
As he was still only 11, because of his young age, a regency was established, headed by their father's cousin Prince Paul of Yugoslavia.
After initially declaring neutrality, on 25 March 1941, although King Peter and his advisors were opposed to Nazi Germany, the Regent, Prince Paul, under immense German pressure signed the Tripartite Pact originally signed by Germany, Italy, and Japan.
Postponing Operation Barbarossa, Germany simultaneously attacked Yugoslavia and Greece.
Within a week, Germany, Bulgaria, Hungary and Italy invaded Yugoslavia and the government was forced to surrender on 17 April.
Yugoslavia was divided to satisfy Italian, Bulgarian, Hungarian and German demands and puppet Croat, Montenegrin and Serb states proclaimed.
However, in 1944, the Tito–Šubašić agreement recognised the Democratic Federal Yugoslavia as a provisional government, with the status of the monarchy to be decided at a later date.
The Federal People's Republic of Yugoslavia was internationally recognized as Yugoslavia while Peter II became a pretender.
Life in exile

After Cambridge, and not being able to return to Yugoslavia following the abolition of the monarchy, Prince Tomislav remained in the UK and devoted himself to fruit growing.
Marriage and issue

He was married on 5 June 1957, in Salem, Baden-Württemberg, West Germany, to Princess Margarita of Baden, niece of Prince Philip, Duke of Edinburgh.
Tomislav and Margarita were divorced in 1981.



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
  AssignClass (903cd37b-d2a7-439c-bff2-93d6df32388f)
 Call ID: 903cd37b-d2a7-439c-bff2-93d6df32388f
  Args:
    type: :Man
    source: :Tomislav_of_Yugoslavia
  AssignClass (0b2de32d-ea38-428e-8a4b-520ac3e2a285)
 Call ID: 0b2de32d-ea38-428e-8a4b-520ac3e2a285
  Args:
    source: :Tomislav_of_Yugoslavia
    type: :Person
  AddLiteral (cb575706-bf16-4fba-82d1-9beed1a45e82)
 Call ID: cb575706-bf16-4fba-82d1-9beed1a45e82
  Args:
    relation: :hasBirthYear
    literal_value: 1928
    literal_type: xsd:positiveInteger
    source: :Tomislav_of_Yugoslavia
  AddLiteral (4acc983e-99b7-4fd3-af55-5b5fe9385c9f)
 Call ID: 4acc983e-99b7-4fd3-af55-5b5fe9385c9f
  Args:
    literal_type: xsd:positiveInteger
    source: :Tomislav_of_Yugoslavia
    relation: :hasDeathYear
    literal_value: 2000
  AssignClass (18ae610a-fee1-4438-a151-4583263ae020)
 Call ID: 18ae610a-fee1-4438-a151-4583263ae020
  Args:
    type: :Man
    source: :Alexander_I_of_Yugoslavia
  AssignClass (bae8841a-49ad-4898-9703-04a9cbfb3b30)
 Call ID: bae8841a-49ad-4898-9703-04a9cbfb3b30
  Args:
    source: :Alexander_I_of_Yugoslavia
    type: :Person
  AssignClass (48e02678-bdba-4007-98bf-60b1f7346256)
 Call ID: 48e02678-bdba-4007-98bf-60b1f7346256
  Args:
    type: :Woman
    source: :Maria_of_Yugoslavia
  AssignClass (e92b1631-5e22-4260-8256-6c6b3efd7eac)
 Call ID: e92b1631-5e22-4260-8256-6c6b3efd7eac
  Args:
    source: :Maria_of_Yugoslavia
    type: :Person
  AddTriple (3743509e-97f5-4ef7-873e-051fcdd06246)
 Call ID: 3743509e-97f5-4ef7-873e-051fcdd06246
  Args:
    target: :Alexander_I_of_Yugoslavia
    source: :Tomislav_of_Yugoslavia
    relation: :hasFather
  AddTriple (2e8ee562-b63a-4ff3-964d-73f5418882a3)
 Call ID: 2e8ee562-b63a-4ff3-964d-73f5418882a3
  Args:
    relation: :hasMother
    source: :Tomislav_of_Yugoslavia
    target: :Maria_of_Yugoslavia
  AssignClass (5df247a0-1419-438f-8fb5-dede7488f256)
 Call ID: 5df247a0-1419-438f-8fb5-dede7488f256
  Args:
    type: :Man
    source: :Peter_II_of_Yugoslavia
  AssignClass (ea714570-9b7d-4b25-80ae-65e8333cdd9c)
 Call ID: ea714570-9b7d-4b25-80ae-65e8333cdd9c
  Args:
    source: :Peter_II_of_Yugoslavia
    type: :Person
  AddTriple (7a9f3aa2-d752-4406-961e-7f89236d82a6)
 Call ID: 7a9f3aa2-d752-4406-961e-7f89236d82a6
  Args:
    source: :Tomislav_of_Yugoslavia
    target: :Peter_II_of_Yugoslavia
    relation: :isBrotherOf
  AssignClass (199a2542-94e7-4bb6-b68d-cb4c274dd717)
 Call ID: 199a2542-94e7-4bb6-b68d-cb4c274dd717
  Args:
    type: :Man
    source: :Ferdinand_of_Romania
  AssignClass (60650267-bac5-4387-a823-a0ecfdb2c954)
 Call ID: 60650267-bac5-4387-a823-a0ecfdb2c954
  Args:
    type: :Person
    source: :Ferdinand_of_Romania
  AssignClass (1195b9b4-ab6d-4f1c-a505-b793e5ba8dbd)
 Call ID: 1195b9b4-ab6d-4f1c-a505-b793e5ba8dbd
  Args:
    source: :Marie_of_Romania
    type: :Woman
  AssignClass (7662aaa5-b687-4a8c-9ecc-9149e66dca07)
 Call ID: 7662aaa5-b687-4a8c-9ecc-9149e66dca07
  Args:
    type: :Person
    source: :Marie_of_Romania
  AddTriple (efd51f7a-7b9f-43a5-a73d-376c7625ba3b)
 Call ID: efd51f7a-7b9f-43a5-a73d-376c7625ba3b
  Args:
    target: :Ferdinand_of_Romania
    source: :Maria_of_Yugoslavia
    relation: :hasFather
  AddTriple (d0c49488-bdb4-4845-b93b-4e5b3833afb4)
 Call ID: d0c49488-bdb4-4845-b93b-4e5b3833afb4
  Args:
    source: :Maria_of_Yugoslavia
    target: :Marie_of_Romania
    relation: :hasMother
  AssignClass (d804d01b-fca2-4bee-abea-f6229e32946e)
 Call ID: d804d01b-fca2-4bee-abea-f6229e32946e
  Args:
    source: :Margarita_of_Baden
    type: :Woman
  AssignClass (201e4588-d0eb-4032-abd0-9ac2447d34d3)
 Call ID: 201e4588-d0eb-4032-abd0-9ac2447d34d3
  Args:
    source: :Margarita_of_Baden
    type: :Person
  AddLiteral (c5ab3482-8173-4a25-80fa-d6730c1eaeb3)
 Call ID: c5ab3482-8173-4a25-80fa-d6730c1eaeb3
  Args:
    literal_type: xsd:positiveInteger
    source: :Tomislav_of_Yugoslavia
    relation: :hasMarriageYear
    literal_value: 1957
  AddTriple (0010594a-c4cf-49df-a6b3-bf99863ba351)
 Call ID: 0010594a-c4cf-49df-a6b3-bf99863ba351
  Args:
    target: :Margarita_of_Baden
    source: :Tomislav_of_Yugoslavia
    relation: :hasRelation
  Finish (3c7555d9-b80c-4369-a3b7-f1eae21d21e4)
 Call ID: 3c7555d9-b80c-4369-a3b7-f1eae21d21e4
  Args: