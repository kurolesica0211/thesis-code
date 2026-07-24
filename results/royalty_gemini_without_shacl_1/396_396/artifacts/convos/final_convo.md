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
Princess Christina Margarethe of Hesse (German: Christina Margarethe Prinzessin von Hessen; 10 January 1933 – 22 November 2011) was a German princess.
Family background and early life

Born in Germany on 10 January 1933 at Friedrichshof Castle near Kronberg im Taunus, Princess Christina ("Krista") of Hesse was the eldest child of Prince Christoph of Hesse (1901–1943) and Princess Sophie of Greece and Denmark (1914–2001)
Her father, Prince Christoph of Hesse, was a nephew of Germany's last emperor Wilhelm II.
Her mother, Princess Sophie of Greece and Denmark, was a grand-daughter of King George I of Greece and a sister of Prince Philip, Duke of Edinburgh.
Christina belonged by birth to the senior line of the House of Hesse, a junior branch of which reigned as grand dukes of Hesse and by Rhine within the German Empire until 1918.
Christina's paternal grandmother, Princess Margaret of Prussia, was a daughter of Queen Victoria's eldest daughter Victoria, and as such a sister of Kaiser Wilhelm II.


Prince Christoph, a member of the Schutzstaffel (SS), held important positions in Germany's Nazi regime.
On 7 October 1943, when Christina was ten years old, her father was killed in an airplane crash in the Apennine Mountains near Forlì, Italy.
His widow married Prince George William of Hanover in 1946.
From her mother's two marriages, Christina had four siblings and three half-siblings: Princess Dorothea of Hesse (1934–2025), Prince Karl of Hesse (1937–2022), Prince Rainer of Hesse (born 1939), Princess Clarissa of Hesse (born 1944), Prince Welf of Hanover (1947–1981), Prince Georg of Hanover (born 1949) and Princess Friederike of Hanover (born 1954).
Her childhood homes included her paternal grandmother's palace of Friedrichshof in Taunus, a family castle at Panker in Holstein, and her parents' residence in Berlin-Dahlem.
Christina participated in the 1953 coronation of her aunt at Westminster Abbey, walking in the procession led by her maternal grandmother, Princess Alice.
Christina and her cousin Princess Beatrix of Hohenlohe-Langenburg spent the winter of 1955-1956 living in London, where Christina studied the restoration of paintings under Anthony Blunt.
It was reported that the princesses' closest friend in England was Prince Andrew of Yugoslavia.
First marriage

Princess Christina of Hesse married Prince Andrew of Yugoslavia, the youngest son of Alexander I of Yugoslavia and Princess Maria of Romania, on 2 August 1956, at Friedrichshof Castle.
They had two children:


Soon after their marriage, Princess Christina and her first husband had purchased The Hollands, a commercial farm at Langton Green in Kent, England, which did not prove a profitable venture.
Moving to London, Prince Andrew supported his family by working for an import/export business and, later, as a bank executive.
In 1961 Christina left her husband to live with an abstract artist from the Netherlands, Robert Floris van Eyck.
Second marriage

Following her divorce, Christina married Robert van Eyck on 3 December 1962 in London.
Her first husband Prince Andrew also married for the second time, this time to another cousin, Princess Kira Melita zu Leiningen (1930–2006).
Christina and Robert van Eyck separated in 1985, and divorced 3 February 1986.
In addition to Germany and England, Princess Christina of Hesse had lived in Saint-Paul-de-Vence, France, and in Gersau, Switzerland.



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
  AssignClass (bd21fc97-41ef-41a5-96d0-db02919b3eb1)
 Call ID: bd21fc97-41ef-41a5-96d0-db02919b3eb1
  Args:
    type: :Woman
    source: :Christina_of_Hesse
  AssignClass (a9fb1b85-0272-4bcf-85dd-51f3ca17cbb3)
 Call ID: a9fb1b85-0272-4bcf-85dd-51f3ca17cbb3
  Args:
    source: :Christoph_of_Hesse
    type: :Man
  AssignClass (f0f77cb3-7208-4cb0-87e1-c8edc729cb70)
 Call ID: f0f77cb3-7208-4cb0-87e1-c8edc729cb70
  Args:
    type: :Woman
    source: :Sophie_of_Greece_and_Denmark
  AddLiteral (b6bd0734-c05b-40d9-ba44-2850378c1d63)
 Call ID: b6bd0734-c05b-40d9-ba44-2850378c1d63
  Args:
    relation: :hasBirthYear
    literal_value: 1933
    source: :Christina_of_Hesse
    literal_type: xsd:integer
  AddLiteral (437d8c32-3478-47a2-85b1-abad173677ec)
 Call ID: 437d8c32-3478-47a2-85b1-abad173677ec
  Args:
    relation: :hasDeathYear
    source: :Christina_of_Hesse
    literal_type: xsd:integer
    literal_value: 2011
  AddTriple (94364ff6-47df-4a0a-bfbc-0b92e247ea07)
 Call ID: 94364ff6-47df-4a0a-bfbc-0b92e247ea07
  Args:
    source: :Christina_of_Hesse
    target: :Christoph_of_Hesse
    relation: :hasFather
  AddTriple (51d29cd7-fe16-4a0b-8bf3-6df68e37051e)
 Call ID: 51d29cd7-fe16-4a0b-8bf3-6df68e37051e
  Args:
    target: :Sophie_of_Greece_and_Denmark
    relation: :hasMother
    source: :Christina_of_Hesse
  AddLiteral (31d4bbac-2726-4f29-92f7-0299aa0e6b69)
 Call ID: 31d4bbac-2726-4f29-92f7-0299aa0e6b69
  Args:
    literal_value: 1901
    literal_type: xsd:integer
    source: :Christoph_of_Hesse
    relation: :hasBirthYear
  AddLiteral (8217fc89-da7f-45db-a46e-ede822d0c944)
 Call ID: 8217fc89-da7f-45db-a46e-ede822d0c944
  Args:
    relation: :hasDeathYear
    literal_value: 1943
    literal_type: xsd:integer
    source: :Christoph_of_Hesse
  AddLiteral (680aaefd-280b-4ac6-aa67-9cd236d9c0dc)
 Call ID: 680aaefd-280b-4ac6-aa67-9cd236d9c0dc
  Args:
    literal_value: 1914
    literal_type: xsd:integer
    source: :Sophie_of_Greece_and_Denmark
    relation: :hasBirthYear
  AddLiteral (1001fc85-e8fa-4028-ae9d-159098dacd21)
 Call ID: 1001fc85-e8fa-4028-ae9d-159098dacd21
  Args:
    relation: :hasDeathYear
    source: :Sophie_of_Greece_and_Denmark
    literal_type: xsd:integer
    literal_value: 2001
  AssignClass (7f71a087-c4b6-4848-bf39-f7cee1211e2a)
 Call ID: 7f71a087-c4b6-4848-bf39-f7cee1211e2a
  Args:
    type: :Man
    source: :George_William_of_Hanover
  AddTriple (df7b1760-e037-455c-9d21-0bf6969c4970)
 Call ID: df7b1760-e037-455c-9d21-0bf6969c4970
  Args:
    source: :Sophie_of_Greece_and_Denmark
    target: :George_William_of_Hanover
    relation: :hasRelation
  AddLiteral (b05c8b4c-8bc9-454c-bf5e-62c0733ba3cd)
 Call ID: b05c8b4c-8bc9-454c-bf5e-62c0733ba3cd
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: :Sophie_of_Greece_and_Denmark
    literal_value: 1946
  AssignClass (9c492bb6-d084-444c-98ce-a217ae904164)
 Call ID: 9c492bb6-d084-444c-98ce-a217ae904164
  Args:
    type: :Woman
    source: :Dorothea_of_Hesse
  AssignClass (8b3fdf40-1b51-4a42-8f6a-76a3981f0eb8)
 Call ID: 8b3fdf40-1b51-4a42-8f6a-76a3981f0eb8
  Args:
    type: :Man
    source: :Karl_of_Hesse
  AssignClass (cd5bac1d-93f7-4130-9f89-7bd4c5414d44)
 Call ID: cd5bac1d-93f7-4130-9f89-7bd4c5414d44
  Args:
    source: :Rainer_of_Hesse
    type: :Man
  AssignClass (e3c8e062-7d11-41a0-af26-6268dd8d9690)
 Call ID: e3c8e062-7d11-41a0-af26-6268dd8d9690
  Args:
    source: :Clarissa_of_Hesse
    type: :Woman
  AssignClass (b4db3cec-e070-4b8f-ac07-94b76f102b5a)
 Call ID: b4db3cec-e070-4b8f-ac07-94b76f102b5a
  Args:
    source: :Welf_of_Hanover
    type: :Man
  AssignClass (118bfbbd-6f32-4f84-b78f-1e04674afd5e)
 Call ID: 118bfbbd-6f32-4f84-b78f-1e04674afd5e
  Args:
    type: :Man
    source: :Georg_of_Hanover
  AssignClass (511dfd3a-4dee-43a3-b6e0-522c211f1f9d)
 Call ID: 511dfd3a-4dee-43a3-b6e0-522c211f1f9d
  Args:
    source: :Friederike_of_Hanover
    type: :Woman
  AddTriple (8ba82a88-4133-4b03-aaea-516cbf58abda)
 Call ID: 8ba82a88-4133-4b03-aaea-516cbf58abda
  Args:
    source: :Christina_of_Hesse
    target: :Dorothea_of_Hesse
    relation: :isSiblingOf
  AddTriple (7e4b3819-a27e-4bf7-a7dd-3c6c8560c21e)
 Call ID: 7e4b3819-a27e-4bf7-a7dd-3c6c8560c21e
  Args:
    target: :Karl_of_Hesse
    relation: :isSiblingOf
    source: :Christina_of_Hesse
  AddTriple (e99a6de1-2635-4d8e-bcc2-db4ca3bcc253)
 Call ID: e99a6de1-2635-4d8e-bcc2-db4ca3bcc253
  Args:
    source: :Christina_of_Hesse
    relation: :isSiblingOf
    target: :Rainer_of_Hesse
  AddTriple (7a93bfcb-a5bd-4cbd-8732-5777260e57ed)
 Call ID: 7a93bfcb-a5bd-4cbd-8732-5777260e57ed
  Args:
    source: :Christina_of_Hesse
    relation: :isSiblingOf
    target: :Clarissa_of_Hesse
  AddTriple (a1a44a67-d028-4bd4-913a-2b0700367f9d)
 Call ID: a1a44a67-d028-4bd4-913a-2b0700367f9d
  Args:
    target: :Welf_of_Hanover
    relation: :isSiblingOf
    source: :Christina_of_Hesse
  AddTriple (e1e6d050-115b-4a5d-be77-216f50d37c38)
 Call ID: e1e6d050-115b-4a5d-be77-216f50d37c38
  Args:
    target: :Georg_of_Hanover
    relation: :isSiblingOf
    source: :Christina_of_Hesse
  AddTriple (25b2c470-05f6-4d44-94fa-2f2fde4245f8)
 Call ID: 25b2c470-05f6-4d44-94fa-2f2fde4245f8
  Args:
    source: :Christina_of_Hesse
    target: :Friederike_of_Hanover
    relation: :isSiblingOf
  AssignClass (ee80dfad-9cfb-42aa-950d-864181ffcd5e)
 Call ID: ee80dfad-9cfb-42aa-950d-864181ffcd5e
  Args:
    type: :Man
    source: :Andrew_of_Yugoslavia
  AddTriple (54c8a586-4220-47b4-b486-77e7ab9d851c)
 Call ID: 54c8a586-4220-47b4-b486-77e7ab9d851c
  Args:
    target: :Andrew_of_Yugoslavia
    relation: :hasRelation
    source: :Christina_of_Hesse
  AddLiteral (a0fa7649-60d1-4604-938d-3c2aa6beeebe)
 Call ID: a0fa7649-60d1-4604-938d-3c2aa6beeebe
  Args:
    literal_value: 1956
    literal_type: xsd:integer
    source: :Christina_of_Hesse
    relation: :hasMarriageYear
  AssignClass (051c1521-41a1-4a40-875a-0857f9661786)
 Call ID: 051c1521-41a1-4a40-875a-0857f9661786
  Args:
    type: :Man
    source: :Robert_van_Eyck
  AddTriple (b95591c7-ea7e-4a34-96d4-2ec586af4688)
 Call ID: b95591c7-ea7e-4a34-96d4-2ec586af4688
  Args:
    source: :Christina_of_Hesse
    target: :Robert_van_Eyck
    relation: :hasRelation
  AddLiteral (54034698-7e89-4f73-bdbc-23e227c2b028)
 Call ID: 54034698-7e89-4f73-bdbc-23e227c2b028
  Args:
    relation: :hasMarriageYear
    literal_value: 1962
    source: :Christina_of_Hesse
    literal_type: xsd:integer
  Finish (b92ad51d-97f2-4d31-a817-75fcd45445f9)
 Call ID: b92ad51d-97f2-4d31-a817-75fcd45445f9
  Args: