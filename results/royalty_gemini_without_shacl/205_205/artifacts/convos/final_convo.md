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
Infanta Beatriz of Spain, Princess of Civitella-Cesi (Beatriz Isabel Federica Alfonsa Eugénie Cristina Maria Teresia Bienvenida Ladislàa de Borbón y Battenberg; 22 June 1909 – 22 November 2002) was a daughter of King Alfonso XIII of Spain and Victoria Eugenie of Battenberg, wife of Alessandro Torlonia, 5th Prince di Civitella-Cesi.
She was a paternal aunt of King Juan Carlos I.


Childhood

Born at the royal palace of La Granja, San Ildefonso near Segovia, Spain on 22 June 1909, Infanta Beatriz was the third child among the six surviving children of King Alfonso XIII of Spain and Victoria Eugenie of Battenberg.
She was named Beatriz after her maternal grandmother, Princess Beatrice of the United Kingdom, the youngest daughter of Queen Victoria; Isabel for her great-aunt, Infanta Isabel; Federica for Princess Frederica of Hanover in whose house her parents had become engaged; Alfonsa after her father; Eugenia for Empress Eugénie of the French, her mother's godmother, Cristina and Maria for Maria Christina of Austria, her paternal grandmother, Teresia after Empress Maria Theresa and Ladislaa after Ladislaus the Posthumous.
Infanta Beatriz was educated within the walls of the Palacio de Oriente by English nannies.
Infanta Beatriz and her sister Maria Cristina, two years her junior, yearned to go to private schools like the daughters of the nobility who frequented the palace as their playmates, but, following Spanish tradition, they were educated by governesses and private tutors.
Their parents placed great importance on outdoor exercise and Infanta Beatriz became fond of sports.
Early life

During the late 1920s, Infanta Beatriz and her sister Infanta Cristina presided at a number of official engagements while heading various institutions and sponsoring events.
Beatriz and her sister took nursing classes, helping twice a week at the Red Cross in Madrid from 9 am to 1 pm and from 3 to 7 pm.
Beatriz was president of the Red Cross in San Sebastián, working there during the royal family's summer vacation.
Beatriz, who resembled her Spanish relatives, was a brunette, tall and lean like her father.
In 1929, Infanta Beatriz turned twenty years old.
She fell in love with Miguel Primo de Rivera y Sáenz de Heredia, the youngest son of Miguel Primo de Rivera, who served as Prime Minister of Spain from 1923 to January 1930 with dictatorial powers.
Because Beatriz and her sister could be carriers of hemophilia, like their mother, King Alphonso XIII was reluctant to follow the tradition of finding husbands for them among Catholic royal princes.
The two sisters' constant companions were their cousins Alvaro, Alonso and Ataúlfo de Orleans y Borbón, the three sons of Infante Alfonso de Orleans y Borbón.
It was expected that Infanta Beatriz would marry Alonso and Maria Cristina, Alvaro, but nothing came out of it as their companionship was interrupted when the turbulent political situation in Spain derailed their lives.
Exile

The support that Alfonso XIII gave to the unpopular dictatorship of Primo de Rivera discredited the king.
Lacking the backing of the military forces, King Alfonso felt obliged to leave the country the same day, but did not abdicate, hoping to be called back to the throne.
Infanta Beatriz, her mother and her siblings, except for Infante Don Juan, who was away on assignment in the Spanish navy, were left behind in Madrid.
The marriage of their parents was unhappy and even in Spain the King and Queen led separate lives.
Queen Victoria Eugenie moved to London and later to Lausanne, Switzerland and the two infantas lived for a time with her.
In 1933 the king moved to Rapallo and as life was too isolated for Beatriz and her sister in Lausanne, they moved with their father to Italy.
At their daughters' insistence, King Alfonso moved to Rome and rented a house for them there.
Infanta Beatriz and her sister became friends with the members of the Italian royal family and quickly adapted to life in Rome.
Beatriz, who was spending summer vacation in Pörtschach am Wörthersee in Austria, was driving a car with her brother Gonzalo as passenger.
Marriage and issue

At the time of her brother's death, Infanta Beatriz was looking forward to her wedding.
While visiting Ostia, she was introduced to an Italian aristocrat, Alessandro Torlonia, 5th Prince di Civitella-Cesi.
Torlonia, who had inherited large estates from his father in 1933, was the son of Marino, 4th Prince di Civitella-Cesi and Mary Elsie Moore, an American heiress.
His family had acquired a fortune in the 18th and 19th centuries by administering the finances of the Vatican, receiving the title of Prince of Civitella-Cesi in 1803 from Pope Pius VII.
Although Don Alessandro was a prince, he did not belong to a reigning or formerly reigning dynasty, so Beatriz had to marry him morganatically, renouncing her rights of succession to the throne of Spain.
Alfonso XIII,
The wedding took place on 14 January 1935 at the Church of the Gesù with Beatriz wearing a 20-foot train, a coronet of orange blossom holding her veil in place, in the presence of King Alfonso, the King and Queen of Italy and some 52 princes of the blood royal.
Thousands of Spaniards traveled from Spain to give support to the deposed royal family in what became a political event.
However, neither Queen Victoria Eugenie nor Beatriz's eldest brother, Alfonso, Count of Covadonga, who were on bad terms with the King, attended the wedding.
Infanta Beatriz of Spain, Princess of Civitella-Cesi, and her husband had four children, eleven grandchildren and nineteen great-grandchildren:


Later life

Infanta Beatriz settled with her husband in the Palazzo Torlonia, a 16th-century Early Renaissance town house on Via della Conciliazione in Rome.
King Alfonso XIII died in 1941 and as the situation deteriorated in Italy during World War II, Infanta Beatriz with her family joined her siblings in Lausanne, spending the rest of the war close to their mother Queen Victoria Eugenie.
Beatriz returned to Italy after the war and dwelt there for the rest of her life.
In 1950, while staying with her brother Juan, in Estoril, Portugal, Infanta Beatriz obtained authorization from Francisco Franco to make a visit to Spain.
She returned to Spain on 25 August 1950 for the first time since her departure to exile almost twenty years earlier.
They stayed at the Ritz hotel in Madrid visiting the palace of la Granja, where the Infanta was born, and the Cathedral-Basilica of Our Lady of the Pillar in Zaragoza.
Infanta Beatriz was received with such a manifestation of support for the monarchy that after only a week, of a planned much longer visit, the government gave her only twenty four hours to leave the country.
Although the family tried to arrange a marriage for the Infanta's daughter, Sandra, with King Baudouin of Belgium, she caused her parents concern when in 1958 she married Clemente Lequio, a widower with a son, who was given the title "Count Lequio di Assaba" in 1963 by Umberto II of Italy.
Their son, Alesandro Lequio, moved to Spain in 1991 working initially for Fiat.
Married to the Italian model Antonia Dell’Atte, a muse in the late 1980s of Giorgio Armani, Alessandro Lequio quickly became a favorite of the Spanish jet set and tabloids, when, after his divorce, he began a relationship with Ana Obregón, a Spanish actress and television presenter.
Infanta Beatriz's eldest son, Marco, married three times and had three children, one in each marriage.
His eldest son, Don Giovanni Torlonia, is a well known designer.
Infanta Beatriz's second son, Marino, died unmarried in 1995 of HIV-related illnesses.
The youngest child, Olimpia, married in 1965 Paul-Annick Weiller (1933–1998), the first son of the aviator Paul-Louis Weiller of the Javal family.
Among their six children is Princess Sibilla of Luxembourg.
Infanta Beatriz remained very fond of Spain and supported the claims to the Spanish throne of her brother Don Juan.
In 1962, she joined the Spanish royal family in the celebration in Athens for the wedding of her nephew the future King Don Juan Carlos with Princess Sophia of Greece.
A femur fracture in 1973 never healed completely, affecting Infanta Beatriz's mobility for the rest of her life.
Her fragile health did not allow her to join her family at the ascension to the throne of King Juan Carlos, the wedding of the Infantas Elena and Cristina or the ceremonies for the return to Spain of the remains of her parents and siblings who had died in exile.
Nevertheless, Infanta Beatriz not only survived all of her siblings, but visited Spain again in 1998 to visit la Granja.
In 1999, the Infanta gave an interview with ¡Hola! Magazine, where she discussed her life and the years of the Royal Family's exile from Spain.
She made her last visit to Spain in 2001 to be with her sister-in-law Doña Maria and returned to the Palacio de la Magdalena, near Santander, where 70 years earlier she had spent her summer vacation for 17 consecutive years until 1930.
She died at her home in Palazzo Torlonia, Rome on 22 November 2002 at 93 years 5 months.
She was the last surviving legitimate child of Alfonso XIII and the last surviving legitimate grandchild of Alfonso XII of Spain.



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
  AssignClass (4f361cf8-e40c-4b81-a3f0-c7a79daa9523)
 Call ID: 4f361cf8-e40c-4b81-a3f0-c7a79daa9523
  Args:
    source: :Infanta_Beatriz_of_Spain
    type: :Woman
  AssignClass (6c72efcc-95ba-4e04-af9c-ad32459ea2d2)
 Call ID: 6c72efcc-95ba-4e04-af9c-ad32459ea2d2
  Args:
    source: :Infanta_Beatriz_of_Spain
    type: :Person
  AddLiteral (dac3c0c2-1970-47cb-adfe-d0303cb79f2f)
 Call ID: dac3c0c2-1970-47cb-adfe-d0303cb79f2f
  Args:
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Beatriz Isabel Federica Alfonsa Eugénie Cristina Maria Teresia Bienvenida Ladislàa de Borbón y Battenberg
    source: :Infanta_Beatriz_of_Spain
  AddLiteral (4b335474-5c40-417a-8053-00fd56c24408)
 Call ID: 4b335474-5c40-417a-8053-00fd56c24408
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1909
    source: :Infanta_Beatriz_of_Spain
  AddLiteral (5eb0f48e-8107-4add-9fc1-abae208cc418)
 Call ID: 5eb0f48e-8107-4add-9fc1-abae208cc418
  Args:
    source: :Infanta_Beatriz_of_Spain
    literal_value: 2002
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (e7027738-03ce-45e4-87a9-fb1ccf86f3f4)
 Call ID: e7027738-03ce-45e4-87a9-fb1ccf86f3f4
  Args:
    source: :King_Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (da54113e-ef3c-4d75-b454-da8b3913a636)
 Call ID: da54113e-ef3c-4d75-b454-da8b3913a636
  Args:
    source: :King_Alfonso_XIII_of_Spain
    type: :Person
  AssignClass (207c1d47-e7bc-42c4-866f-ce8391b8d5ab)
 Call ID: 207c1d47-e7bc-42c4-866f-ce8391b8d5ab
  Args:
    source: :Victoria_Eugenie_of_Battenberg
    type: :Woman
  AssignClass (6f4ae42a-44cc-4015-afdb-b744c8a34310)
 Call ID: 6f4ae42a-44cc-4015-afdb-b744c8a34310
  Args:
    source: :Victoria_Eugenie_of_Battenberg
    type: :Person
  AddTriple (9773fcd9-ae3b-4033-9508-2e100632d97d)
 Call ID: 9773fcd9-ae3b-4033-9508-2e100632d97d
  Args:
    target: :King_Alfonso_XIII_of_Spain
    source: :Infanta_Beatriz_of_Spain
    relation: :hasFather
  AddTriple (281261a0-1d0f-4cfd-88f7-b64f0e22b5ac)
 Call ID: 281261a0-1d0f-4cfd-88f7-b64f0e22b5ac
  Args:
    relation: :hasMother
    source: :Infanta_Beatriz_of_Spain
    target: :Victoria_Eugenie_of_Battenberg
  AssignClass (31eb921c-50a0-46b0-b70e-0a1699255328)
 Call ID: 31eb921c-50a0-46b0-b70e-0a1699255328
  Args:
    source: :Alessandro_Torlonia
    type: :Man
  AssignClass (40b23c0d-2e20-4a9e-aca7-ccaa3fad823c)
 Call ID: 40b23c0d-2e20-4a9e-aca7-ccaa3fad823c
  Args:
    source: :Alessandro_Torlonia_5th_Prince_di_Civitella_Cesi
    type: :Man
  AssignClass (6215a29f-1135-42c0-a56e-404626bd76ab)
 Call ID: 6215a29f-1135-42c0-a56e-404626bd76ab
  Args:
    source: :Alessandro_Torlonia_5th_Prince_di_Civitella_Cesi
    type: :Person
  AddTriple (f5681c89-f3f6-453b-9e7c-10f55d977f7b)
 Call ID: f5681c89-f3f6-453b-9e7c-10f55d977f7b
  Args:
    relation: :hasRelation
    target: :Alessandro_Torlonia_5th_Prince_di_Civitella_Cesi
    source: :Infanta_Beatriz_of_Spain
  AddLiteral (1889c52a-23df-41d5-a33c-530f166af6a6)
 Call ID: 1889c52a-23df-41d5-a33c-530f166af6a6
  Args:
    source: :Infanta_Beatriz_of_Spain
    literal_value: 1935
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AssignClass (3c6a6b67-9db5-4fa9-996f-800f731d09c9)
 Call ID: 3c6a6b67-9db5-4fa9-996f-800f731d09c9
  Args:
    source: :King_Juan_Carlos_I
    type: :Man
  AssignClass (5e3b8d52-0f91-45f6-b68b-b0ad5abd0bd6)
 Call ID: 5e3b8d52-0f91-45f6-b68b-b0ad5abd0bd6
  Args:
    source: :King_Juan_Carlos_I
    type: :Person
  AddTriple (b0dce79e-7964-41e3-8ccd-c830736c1cbd)
 Call ID: b0dce79e-7964-41e3-8ccd-c830736c1cbd
  Args:
    source: :Infanta_Beatriz_of_Spain
    target: :King_Juan_Carlos_I
    relation: :isAuntOf
  AssignClass (fa60a3c9-5791-457c-bd92-a04b1174fd5a)
 Call ID: fa60a3c9-5791-457c-bd92-a04b1174fd5a
  Args:
    source: :Maria_Cristina
    type: :Woman
  AssignClass (e780f2e3-6b7c-4bdc-bc48-013479adf4d7)
 Call ID: e780f2e3-6b7c-4bdc-bc48-013479adf4d7
  Args:
    source: :Maria_Cristina
    type: :Person
  AddTriple (44b374c8-aa29-4f05-be3f-33b352272182)
 Call ID: 44b374c8-aa29-4f05-be3f-33b352272182
  Args:
    relation: :hasSister
    target: :Maria_Cristina
    source: :Infanta_Beatriz_of_Spain
  AssignClass (09480d12-185c-4c3d-a3c2-50ea7e314880)
 Call ID: 09480d12-185c-4c3d-a3c2-50ea7e314880
  Args:
    source: :Gonzalo
    type: :Man
  AssignClass (2a9496c9-52be-4004-8912-8d271621ece0)
 Call ID: 2a9496c9-52be-4004-8912-8d271621ece0
  Args:
    source: :Gonzalo
    type: :Person
  AddTriple (23ecdb25-8350-4863-8548-3b08e2d15fd4)
 Call ID: 23ecdb25-8350-4863-8548-3b08e2d15fd4
  Args:
    target: :Gonzalo
    source: :Infanta_Beatriz_of_Spain
    relation: :hasBrother
  AssignClass (7117c13b-cf63-4dad-966b-0cbb485e03f6)
 Call ID: 7117c13b-cf63-4dad-966b-0cbb485e03f6
  Args:
    source: :Don_Juan
    type: :Man
  AssignClass (5d07753c-503e-4c69-a69b-f28e7d178817)
 Call ID: 5d07753c-503e-4c69-a69b-f28e7d178817
  Args:
    source: :Don_Juan
    type: :Person
  AddTriple (1c661327-0b33-498c-baae-923bc131d959)
 Call ID: 1c661327-0b33-498c-baae-923bc131d959
  Args:
    target: :Don_Juan
    source: :Infanta_Beatriz_of_Spain
    relation: :hasBrother
  AssignClass (47d51e66-d79e-4840-ade0-5834586e8cec)
 Call ID: 47d51e66-d79e-4840-ade0-5834586e8cec
  Args:
    source: :Alfonso_Count_of_Covadonga
    type: :Man
  AssignClass (019d0f45-6762-4d7e-a905-2120469005e2)
 Call ID: 019d0f45-6762-4d7e-a905-2120469005e2
  Args:
    source: :Alfonso_Count_of_Covadonga
    type: :Person
  AddTriple (9a09b8e7-1b7f-4b44-8ce7-5cd069dff560)
 Call ID: 9a09b8e7-1b7f-4b44-8ce7-5cd069dff560
  Args:
    relation: :hasBrother
    source: :Infanta_Beatriz_of_Spain
    target: :Alfonso_Count_of_Covadonga
  AssignClass (550f5dbe-2d77-40ef-acce-83fbed68b034)
 Call ID: 550f5dbe-2d77-40ef-acce-83fbed68b034
  Args:
    source: :Sandra
    type: :Woman
  AssignClass (c61abe70-9cbe-4103-b965-fb6f41590de5)
 Call ID: c61abe70-9cbe-4103-b965-fb6f41590de5
  Args:
    source: :Sandra
    type: :Person
  AddTriple (72faff96-63ef-402e-baa2-f587613f082f)
 Call ID: 72faff96-63ef-402e-baa2-f587613f082f
  Args:
    relation: :hasDaughter
    target: :Sandra
    source: :Infanta_Beatriz_of_Spain
  AssignClass (90f8c367-2a71-4526-bb66-6c2d7bd72fae)
 Call ID: 90f8c367-2a71-4526-bb66-6c2d7bd72fae
  Args:
    source: :Marco
    type: :Man
  AssignClass (7bfab879-46bd-4ed9-bf40-6eb1418e753f)
 Call ID: 7bfab879-46bd-4ed9-bf40-6eb1418e753f
  Args:
    source: :Marco
    type: :Person
  AddTriple (650e1ab8-6034-43d2-be07-7fc8beeb18c9)
 Call ID: 650e1ab8-6034-43d2-be07-7fc8beeb18c9
  Args:
    target: :Marco
    source: :Infanta_Beatriz_of_Spain
    relation: :hasSon
  AssignClass (c6fc5c2b-7834-4a5c-9aa4-0e897f874f28)
 Call ID: c6fc5c2b-7834-4a5c-9aa4-0e897f874f28
  Args:
    source: :Marino_son_of_Beatriz
    type: :Man
  AssignClass (35cc88a6-9750-47f3-9f15-84e20464eff4)
 Call ID: 35cc88a6-9750-47f3-9f15-84e20464eff4
  Args:
    source: :Marino_son_of_Beatriz
    type: :Person
  AddTriple (cba741dc-dc62-46da-9c71-79c179ad4e8a)
 Call ID: cba741dc-dc62-46da-9c71-79c179ad4e8a
  Args:
    relation: :hasSon
    source: :Infanta_Beatriz_of_Spain
    target: :Marino_son_of_Beatriz
  AssignClass (dcff2c92-f4b7-4b62-b186-707f11dfcfb8)
 Call ID: dcff2c92-f4b7-4b62-b186-707f11dfcfb8
  Args:
    source: :Olimpia
    type: :Woman
  AssignClass (5b755489-6ebd-4a73-a9cc-6a943cc8010d)
 Call ID: 5b755489-6ebd-4a73-a9cc-6a943cc8010d
  Args:
    source: :Olimpia
    type: :Person
  AddTriple (ba630386-8eda-45b7-afc7-335d2e443157)
 Call ID: ba630386-8eda-45b7-afc7-335d2e443157
  Args:
    target: :Olimpia
    source: :Infanta_Beatriz_of_Spain
    relation: :hasDaughter
  Finish (43363a3b-a3f2-49fd-97ab-d9694a6f1d9f)
 Call ID: 43363a3b-a3f2-49fd-97ab-d9694a6f1d9f
  Args: